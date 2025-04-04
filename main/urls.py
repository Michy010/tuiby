from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('filter_sellers/', views.filter_sellers, name='buyer'),
    path('seller/',views.for_seller, name='seller'),
    path('faqs/', views.faqs_views, name='faqs'),
    path('electronics-product-list/', views.electronics_product_list, name='electronics-product-list'),
    path('fashion-product-list/', views.fashion_product_list, name='fashion-product-list'),
    path('furniture-product-list/', views.furniture_product_list, name='furniture-product-list'),
    path('kitchenware-product-list/', views.kitchenware_product_list, name='kitchenware-product-list'),
    path('update-location/', views.update_location, name = 'location-update'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('update-product/', views.update_product_view, name='update-product'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-social-handle/', views.social_media_infos, name='add-social-handle'),
]