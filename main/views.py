import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import SellerLocation, SocialInfo, ProductInfo
from .utils import haversine  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

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
            distance = haversine(user_latitude, user_longitude, seller_lat, seller_lon)

            # Get product info for the seller based on search query
            product_info = ProductInfo.objects.filter(user=seller.user, product_name__icontains=query).first()
            if product_info:
                # Get all social handles linked to the product
                social_handles = SocialInfo.objects.filter(product_infos=product_info)

                sellers.append({
                    "distance": round(distance, 2),  # Rounded for better UI
                    "product_info": product_info,
                    "social_handles": social_handles
                })
        except ValueError:
            continue  # Skip sellers with invalid coordinates

    # Sort sellers by nearest distance
    sellers = sorted(sellers, key=lambda x: x["distance"])

    return render(request, 'main/for_buyer.html', {"sellers": sellers, "query": query})

def for_seller(request):
    return render (request, 'main/for_seller.html')

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
            return redirect("dashboard") 
    
    return render(request, "main/SellerLocation.html")



@login_required
def edit_profile(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_pic = request.FILES.get("profile_pic")

        user = request.user
        user.first_name, user.last_name = full_name.split(" ", 1) if " " in full_name else (full_name, "")
        user.email = email
        
        if password:
            user.set_password(password)
        
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("edit_profile")
    
    return render(request, "main/Edit_profile.html")

def update_product_view(request):
    return render(request, 'main/GotoProduct.html')