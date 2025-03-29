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

@csrf_exempt
def for_buyer(request):
    if request.method == 'POST':
        try:
            # Decode and parse request body
            location_dict = json.loads(request.body.decode('utf-8'))
            
            lat1 = float(location_dict.get('latitude', 0))
            lon1 = float(location_dict.get('longitude', 0))

            sellers_list = []
            for seller in SellerLocation.objects.select_related('user'):
                user = seller.user

                # Get seller information efficiently
                seller_dict = {
                    'lat2': seller.latitude,
                    'lon2': seller.longitude,
                    'handle': list(SocialInfo.objects.filter(user=user).values_list('handle', flat=True)),
                    'name': list(ProductInfo.objects.filter(user=user).values_list('product_name', flat=True)),
                    'description': list(ProductInfo.objects.filter(user=user).values_list('product_descriptions', flat=True))
                }

                # Calculate distance
                distance = haversine(lat1, lon1, seller_dict['lat2'], seller_dict['lon2'])

                # Append seller data
                sellers_list.append({
                    'handle': seller_dict['handle'],
                    'name': seller_dict['name'],
                    'description': seller_dict['description'],
                    'distance': distance
                })

            # Sort sellers by distance
            sorted_list = sorted(sellers_list, key=lambda x: x['distance'])
            return JsonResponse({'sellers': sorted_list}, safe=False)

        except Exception as e:
            return JsonResponse({'Error': str(e)}, status=400)

    elif request.method == 'GET':
        query = request.GET.get('query', '').strip().lower()

        if not query:
            return render(request, 'main/for_buyer.html', {'list': []})

        # Optimize filtering with ORM
        sellers = SellerLocation.objects.filter(
            Q(productinfo__product_name__icontains=query) |
            Q(productinfo__product_descriptions__icontains=query)
        ).distinct()

        sellers_list = [
            {
                'handle': list(SocialInfo.objects.filter(user=seller.user).values_list('handle', flat=True)),
                'name': list(ProductInfo.objects.filter(user=seller.user).values_list('product_name', flat=True)),
                'description': list(ProductInfo.objects.filter(user=seller.user).values_list('product_descriptions', flat=True)),
            }
            for seller in sellers
        ]

        return render(request, 'main/for_buyer.html', {'sellers': sellers_list})

def get_buyer_location(request):
    if request.method == 'POST':
        location = json.loads(request.body)
        lat1 = float(location.get('latitude', 0))
        lon1 = float(location.get('longitude', 0))

        request.session['lat1'] = lat1
        request.session['lon1'] = lon1

    return JsonResponse ({'success': 'Latitude and longitude have successful stored in sessions'})

def get_search_result(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        seller = SellerLocation.objects.filter(
            Q(productinfo__product_name__icontains=query) | Q(productinfo__descriptions__icontains=query)
        )

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
        
        if profile_pic:
            user.profile.image = profile_pic 

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("edit_profile")
    
    return render(request, "main/Edit_profile.html")

def update_product_view(request):
    return render(request, 'main/GotoProduct.html')