import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Q , Sum
from .models import SellerLocation, SocialInfo, ProductInfo, BusinessProfile, Statistic
from accounts.models import CustomUser
from .utils import vincenty_distance  
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib import messages
from .forms import ProductForm, SocialInfoForm, SellerLocationForm
from django.core.paginator import Paginator
from django.urls import reverse
from datetime import timedelta, date


def index(request):
    return render (request, 'main/index.html')


def filter_sellers(request):
    platform = request.GET.get('platform')
    location = request.GET.get('location', '').strip()
    query = request.GET.get('query', '').strip()

    try:
        user_latitude = float(request.GET.get('latitude', 0))
        user_longitude = float(request.GET.get('longitude', 0))
    except ValueError:
        return render(request, 'main/for_buyer.html', {"sellers": [], "query": query, "error": "Invalid location data."})

    flattened_sellers = []

    all_seller_locations = SellerLocation.objects.select_related('user').all()

    for seller in all_seller_locations:
        try:
            seller_lat = float(seller.latitude)
            seller_lon = float(seller.longitude)
            distance = vincenty_distance(user_latitude, user_longitude, seller_lat, seller_lon)

            # Filter social handles first
            social_filter = Q(user=seller.user)
            if platform and platform != "all":
                social_filter &= Q(social_category__iexact=platform)

            social_handles = SocialInfo.objects.filter(social_filter)

            for social in social_handles:
                product_info = social.product_infos

                # Apply product name/description filter
                if query:
                    if query.lower() not in product_info.product_name.lower() and \
                       query.lower() not in product_info.product_descriptions.lower():
                        continue

                # Apply location filter
                if location and location.lower() not in seller.location.lower():
                    continue

                # Track statistics
                today = date.today()
                stat, _ = Statistic.objects.get_or_create(user=seller.user, date_time=today)
                stat.appearence_count += 1
                stat.save()

                # Append data
                flattened_sellers.append({
                    "user": seller.user,
                    "distance": round(distance, 2),
                    "product_info": product_info,
                    "social": social
                })

        except ValueError:
            continue

    # Sort by distance
    flattened_sellers = sorted(flattened_sellers, key=lambda x: x["distance"])

    # Pagination
    paginator = Paginator(flattened_sellers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/for_buyer.html', {
        "sellers": page_obj,
        "query": query,
    })

def for_seller(request):
    return render (request, 'main/for_seller.html')

def seller_panel(request):
    handle=''
    user = request.user
    products = ProductInfo.objects.filter(user=user)
    handle = SocialInfo.objects.filter(user=user)
    today = date.today()
    last_week = today - timedelta(days=7)

    # This week
    current_stats = Statistic.objects.filter(user=user, date_time__gte=last_week, date_time__lte=today)
    current_appear = current_stats.aggregate(Sum('appearence_count'))['appearence_count__sum'] or 0
    current_copied = current_stats.aggregate(Sum('link_copied_count'))['link_copied_count__sum'] or 0

    # Previous week
    prev_start = last_week - timedelta(days=7)
    previous_stats = Statistic.objects.filter(user=user, date_time__gte=prev_start, date_time__lt=last_week)
    previous_appear = previous_stats.aggregate(Sum('appearence_count'))['appearence_count__sum'] or 0
    previous_copied = previous_stats.aggregate(Sum('link_copied_count'))['link_copied_count__sum'] or 0

    # Differences
    diff_appear = current_appear - previous_appear
    diff_copied = current_copied - previous_copied

    context = {
        'current_appear': current_appear,
        'current_copied': current_copied,
        'diff_appear': diff_appear,
        'diff_copied': diff_copied,
        'products':products,
        'social':handle

    }
    return render(request, 'main/seller_panel.html', context)


def faqs_views(request):
    return render(request, 'main/faqs.html')

def update_location(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        location = request.POST.get('location')
        
        if latitude and longitude:
            SellerLocation.objects.update_or_create(
                user=request.user,
                defaults={"latitude": latitude, "longitude": longitude, "location":location}
            )
            return redirect('main:product-list') 
    
    return render(request, "main/seller_panel.html")


def edit_profile(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        location = request.POST.get("location")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        instagram = request.POST.get("instagram")
        facebook = request.POST.get("facebook")
        tiktok = request.POST.get("tiktok")
        business_name = request.POST.get('business_name')
        business_descriptions = request.POST.get('business_descriptions')

        print(location)

        user = request.user
        if full_name:
            CustomUser.objects.update_or_create(
                email=user.email,
                defaults={'full_name':full_name}
            )
        if location:
            SellerLocation.objects.update_or_create(
                user=user,
                defaults={'location': location, 'latitude':latitude, 'longitude':longitude}
            )
        
        if instagram:
            SocialInfo.objects.update_or_create(
                social_category='instagram',
                defaults={'handle':instagram, 'social_category':'instagram'}
            )
        if facebook:
            SocialInfo.objects.update_or_create(
                social_category='facebook',
                defaults={'handle':facebook, 'social_category':'facebook'}
            )
        if tiktok:
            SocialInfo.objects.update_or_create(
                social_category='tiktok',
                defaults={'handle':tiktok, 'social_category':'tiktok'}
            )
        if business_name:
            BusinessProfile.objects.update_or_create(
                user=user,
                defaults={'business_name':business_name}
            )
        if business_descriptions:
            BusinessProfile.objects.update_or_create(
                user=user,
                defaults={'business_descriptions':business_descriptions}
            )
        
        # user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("main:edit-profile")
    
    return render(request, "main/seller_panel.html")

def update_product_view(request):
    return render(request, 'main/product_list.html')

def product_list(request):
    user = request.user
    products = ProductInfo.objects.filter(user=user)
    fashion = []
    furniture = []
    electronics = []
    kitchenware = []
    other = []
    for product in products:
        if product.product_category =='Fashion':
            fashion.append(product)
        elif product.product_category == 'Furniture':
            furniture.append(product)
        elif product.product_category == 'Electronics':
            electronics.append(product)
        elif product.product_category == 'Kitchenware':
            kitchenware.append(product)
        else:
            other.append(product)
    return render (request, 'main/product_list.html', {'products':products})

def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        product_descriptions = request.POST.get('description')
        product_category = request.POST.get('category')

        user = request.user

        ProductInfo.objects.create(
            user=user,
            product_name=product_name,
            product_descriptions=product_descriptions,
            product_category=product_category
        )

        url = reverse('main:seller-panel')
        return redirect(f'{url}#products')

    return render(request, 'main/seller_panel.html')


# EDIT PAGE VIEWS
def edit_product_info(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk, user=request.user)
    # social = SocialInfo.objects.filter(product_infos=product).first()
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        # social_form = SocialInfoForm(request.POST, instance=social)
        if form.is_valid(): #and social_form.is_valid():
            form.save()
            messages.success(request, 'Changes successful updated')
            return redirect('main:edit-product', product.pk)
    else:
        form = ProductForm(instance=product)
        # social_form = SocialInfoForm(instance=social)
    return render(request, 'main/edit_product_info.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk, user=request.user)

    if request.method == 'POST':
        product_name = product.product_name 
        product.delete()
        messages.success(request, f'{product_name} was deleted successfully!')
        url = reverse('main:seller-panel')
        return redirect(f'{url}#products')

    return render(request, 'main/confirm_delete.html', {'product': product})


@csrf_exempt  
def update_statistics(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        handle_id = data.get('handle_id')

        try:
            user = CustomUser.objects.get(id=handle_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Check if Statistic exists; if not, create it
        today = date.today()
        statistic, created = Statistic.objects.get_or_create(user=user, date_time=today)
        statistic.link_copied_count += 1
        statistic.save()

        return JsonResponse({
            'success': 'Link copy count updated',
            'new_count': statistic.link_copied_count,
            'created': created
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
