from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'main'

urlpatterns = [
    # Home url
    path('', views.index, name='home'),

    # Seller related urls
    path('filter_sellers/', views.filter_sellers, name='buyer'),
    path('seller/',views.for_seller, name='seller'),
    path('faqs/', views.faqs_views, name='faqs'),
    path('seller-panel/', views.seller_panel, name='seller-panel'),

    
    # Profile related urls
    path('edit-profile/', views.edit_profile, name='edit-profile'),

    # Product related urls
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),

    # EDIT URLS
    path('edit-product/product/<int:pk>/', views.edit_product_info, name='edit-product'),

    path('update-statistics/', views.update_statistics, name='update-statistics'),

    # Robots.txt
    path('robots.txt', TemplateView.as_view(template_name='main/robots.txt', content_type='text/plain'))
]