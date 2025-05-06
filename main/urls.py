from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Home url
    path('', views.index, name='home'),

    # Seller related urls
    path('filter_sellers/', views.filter_sellers, name='buyer'),
    path('seller/',views.for_seller, name='seller'),
    path('faqs/', views.faqs_views, name='faqs'),
    path('seller-panel/', views.seller_panel, name='seller-panel'),

    # Social infos 
    # path('add-social-handle/', views.socialView, name='add-social-handle'),

    # Location related urls
    path('update-location/', views.update_location, name = 'location-update'),

    # Profile related urls
    path('edit-profile/', views.edit_profile, name='edit-profile'),

    # Product related urls
    path('product-list/', views.product_list, name='product-list'),
    path('update-product/', views.update_product_view, name='update-product'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),

    # EDIT URLS
    path('edit-product/product/<int:pk>/', views.edit_product_info, name='edit-product'),

    path('update-statistics/', views.update_statistics, name='update-statistics'),
]