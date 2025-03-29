from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('filter_sellers/', views.filter_sellers, name='buyer'),
    path('seller/',views.for_seller, name='seller'),
    path('faqs/', views.faqs_views, name='faqs'),
    # path('send-location/', views.filter_sellers, name='location'),
    path('update-location/', views.update_location, name = 'location-update'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('update-product/', views.update_product_view, name='update-product'),
]