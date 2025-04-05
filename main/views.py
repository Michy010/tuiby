import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import SellerLocation, SocialInfo, ProductInfo
from .utils import haversine, vincenty_distance  
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProductForm, SocialInfoForm, SellerLocationForm


def index(request):
    return render (request, 'main/index.html')

# Filter sellers based on user's location and query
def filter_sellers(request):
    query = request.GET.get('query', '').strip()
    try:
        user_latitude = float(request.GET.get('latitude', 0))
        user_longitude = float(request.GET.get('longitude', 0))
    except ValueError:
        return render(request, 'main/for_buyer.html', {"sellers": [], "query": query, "error": "Invalid location data."})

    sellers = []
    seller_locations = SellerLocation.objects.select_related('user').all()

    for seller in seller_locations:
        try:
            seller_lat = float(seller.latitude)
            seller_lon = float(seller.longitude)
            distance = vincenty_distance(user_latitude, user_longitude, seller_lat, seller_lon)

            # Get product info for the seller based on search query
            product_info = ProductInfo.objects.filter(user=seller.user, product_name__icontains=query).first()
            if product_info:
                # Get all social handles linked to the product
                social_handles = SocialInfo.objects.filter(product_infos=product_info)

                sellers.append({
                    "distance": round(distance, 2),
                    "product_info": product_info,
                    "social_handles": social_handles
                })
        except ValueError:
            continue 

    # Sort sellers by nearest distance
    sellers = sorted(sellers, key=lambda x: x["distance"])

    return render(request, 'main/for_buyer.html', {"sellers": sellers, "query": query})

def for_seller(request):
    product = ProductInfo.objects.filter(user=request.user).first()
    location = SellerLocation.objects.filter(user=request.user).first()
    social = SocialInfo.objects.filter(product_infos__user=request.user).first()
    return render (request, 'main/for_seller.html', {
        'product': product,
        'location': location,
        'social': social,
    })

def faqs_views(request):
    return render(request, 'main/faqs.html')


@login_required
def update_location(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        
        if latitude and longitude:
            SellerLocation.objects.update_or_create(
                user=request.user,
                defaults={"latitude": latitude, "longitude": longitude}
            )
            return redirect('main:product-list') 
    
    return render(request, "main/SellerLocation.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = request.user
        user.username = username
        user.email = email
        
        if password:
            user.set_password(password)
        
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("main:edit-profile")
    
    return render(request, "main/Edit_profile.html")

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
    return render (request, 'main/product_list.html', {
        'products': {
            'Electronics': electronics,
            'Fashion': fashion,
            'Kitchenware':kitchenware,
            'Other':other,
            'Furniture':furniture
        }
    })

@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()
            return redirect('main:product-list') 
    else:
        form = ProductForm()
    
    return render(request, 'main/add_product.html', {'form': form})

@login_required  
def social_media_infos(request):
    if request.method == "POST":
        form = SocialInfoForm(request.POST)
        if form.is_valid():
            social_info = form.save(commit=False) 
            social_info.user = request.user  
            social_info.save()
            messages.success (request, 'Social media handle saved successful')  
            return redirect('main:add-social-handle') 
    else:
        form = SocialInfoForm()
    
    return render(request, 'main/social_media_infos.html', {'form': form})

# EDIT PAGE VIEWS
@login_required
def edit_product_info(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes successful updated')
            return redirect('main:edit-product', product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/edit_product_info.html', {'form': form, 'product': product})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(ProductInfo, pk=pk, user=request.user)

    if request.method == 'POST':
        product_name = product.product_name 
        product.delete()
        messages.success(request, f'{product_name} was deleted successfully!')
        return redirect('main:product-list')

    return render(request, 'main/confirm_delete.html', {'product': product})


@login_required
def edit_social_info(request, pk):
    social = get_object_or_404(SocialInfo, pk=pk, product_infos__user=request.user)
    if request.method == 'POST':
        form = SocialInfoForm(request.POST, instance=social)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes successful updated')
            return redirect('main:edit_social', social.pk)
    else:
        form = SocialInfoForm(instance=social)
    return render(request, 'main/edit_social_info.html', {'form': form}, {'social':social})