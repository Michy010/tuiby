import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Q , Sum,F
from .models import SellerLocation, SocialInfo, ProductInfo, BusinessProfile, Statistic
from accounts.models import CustomUser
from .utils import vincenty_distance, get_profile_completion
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
        return render(request, 'main/for_buyer.html', {
            "sellers": [],
            "query": query,
            "error": "Invalid location data."
        })

    flattened_sellers = []

    all_seller_locations = SellerLocation.objects.select_related('user').all()

    for seller in all_seller_locations:
        try:
            seller_lat = float(seller.latitude)
            seller_lon = float(seller.longitude)
            distance = vincenty_distance(user_latitude, user_longitude, seller_lat, seller_lon)

            # Get all social handles for the seller
            all_socials = SocialInfo.objects.filter(user=seller.user)

            if platform and platform != "all":
                all_socials = all_socials.filter(social_category__iexact=platform)

            for social in all_socials:
                linked_products = social.product_infos.all()

                # Filter products by query
                if query:
                    linked_products = linked_products.filter(
                        Q(product_name__icontains=query) |
                        Q(product_descriptions__icontains=query)
                    )

                for product in linked_products:
                    # Location filter
                    if location and location.lower() not in seller.location.lower():
                        continue

                    # Track stats
                    today = date.today()
                    stat, _ = Statistic.objects.get_or_create(user=seller.user, date_time=today)
                    Statistic.objects.filter(id=stat.id).update(appearence_count=F('appearence_count') + 1)

                    flattened_sellers.append({
                        "user": seller.user,
                        "distance": round(distance, 2),
                        "product_info": product,
                        "social": social
                    })

        except ValueError:
            continue

    # Sort by distance
    flattened_sellers = sorted(flattened_sellers, key=lambda x: x["distance"])

    # Paginate
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

    completion = get_profile_completion(request.user)

    location = user.sellerlocation.first()

    context = {
        'completion':completion,
        'current_appear': current_appear,
        'current_copied': current_copied,
        'diff_appear': diff_appear,
        'diff_copied': diff_copied,
        'products':products,
        'social':handle,
        'location':location,

    }
    return render(request, 'main/seller_panel.html', context)


def faqs_views(request):
    return render(request, 'main/faqs.html')



def edit_profile(request):
    if request.method == "POST":
        user = request.user

        # Get form values
        full_name = request.POST.get("full_name")
        location = request.POST.get("location")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        instagram = request.POST.get("instagram")
        facebook = request.POST.get("facebook")
        tiktok = request.POST.get("tiktok")
        business_name = request.POST.get('business_name')
        business_descriptions = request.POST.get('business_descriptions')
        product_category = request.POST.get('product_category')

        # Update full name
        if full_name:
            CustomUser.objects.update_or_create(
                email=user.email,
                defaults={'full_name': full_name}
            )

        # Update or create seller location
        if location:
            SellerLocation.objects.update_or_create(
                user=user,
                defaults={
                    'location': location,
                    'latitude': latitude,
                    'longitude': longitude
                }
            )

        # Update or create BusinessProfile
        business_profile, _ = BusinessProfile.objects.update_or_create(
            user=user,
            defaults={
                'business_name': business_name if business_name else '',
                'business_descriptions': business_descriptions if business_descriptions else '',
                'product_category': product_category if product_category else 'Other'
            }
        )

        # Get all user's products
        user_products = ProductInfo.objects.filter(user=user)

        # If no products exist, create a default one
        if not user_products.exists():
            default_product = ProductInfo.objects.create(
                user=user,
                business_profile=business_profile,
                product_name="Default Product",
                product_descriptions="Auto-created product for social links"
            )
            user_products = [default_product]

        # Save or update social handles
        socials = {
            'Facebook': facebook,
            'Instagram': instagram,
            'Tiktok': tiktok,
        }

        for category, handle in socials.items():
            if handle:
                if not handle.startswith('@'):
                    messages.error(request, f"{category} handle must start with '@'")
                    continue

                # Update or create social handle
                social_obj, _ = SocialInfo.objects.update_or_create(
                    user=user,
                    social_category=category,
                    defaults={'handle': handle}
                )

                # Associate with all user's products
                social_obj.product_infos.set(user_products)

        messages.success(request, "Profile updated successfully!")
        return redirect("main:edit-profile")

    return render(request, "main/seller_panel.html")


def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        product_descriptions = request.POST.get('description')

        user = request.user

        # Step 1: Get the business profile of the current user
        business_profile = BusinessProfile.objects.filter(user=user).first()

        if business_profile:
            # Step 2: Create the product
            product = ProductInfo.objects.create(
                user=user,
                product_name=product_name,
                product_descriptions=product_descriptions,
                business_profile=business_profile
            )

            # Step 3: Get all social handles of the user
            social_handles = SocialInfo.objects.filter(user=user)

            # Step 4: Associate the product with each social handle (ManyToMany)
            for social in social_handles:
                social.product_infos.add(product)

            messages.success(request, "Product added and associated with your social handles successfully!")
        else:
            messages.error(request, "You must first create a business profile before adding products.")

        # Redirect back to seller panel
        url = reverse('main:seller-panel')
        return redirect(f'{url}#products')

    return render(request, 'main/seller_panel.html')

def edit_product_info(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product details updated successfully.')
            return redirect('main:edit-product', product.pk)
    else:
        form = ProductForm(instance=product)

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
