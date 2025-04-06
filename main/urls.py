from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('filter_sellers/', views.filter_sellers, name='buyer'),
    path('seller/',views.for_seller, name='seller'),
    path('faqs/', views.faqs_views, name='faqs'),
    path('product-list/', views.product_list, name='product-list'),
    path('update-location/', views.update_location, name = 'location-update'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('update-product/', views.update_product_view, name='update-product'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),
    # path('add-social-handle/', views.social_media_infos, name='add-social-handle'),

    # EDIT URLS
    path('edit-product/product/<int:pk>/', views.edit_product_info, name='edit-product'),
]