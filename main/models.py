from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_handle_input(value):
    if not value.startswith('@'):
        raise ValidationError('The handle should start with "@"')

# Create your models here.
class ProductInfo(models.Model):
    PRODUCT_CATEGORIES = [
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Furniture', 'Furniture'),
        ('Kitchenware', 'Kitchenware'),
        ('Other', 'other')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=15)
    product_descriptions = models.CharField(max_length=100)
    product_category = models.CharField(max_length=15, choices=PRODUCT_CATEGORIES, default='Fashion')

    def __str__(self):
        return self.product_name
    
class SocialInfo(models.Model):
    SOCIAL_CATEGORIES = [
        ('Facebook', 'facebook'),
        ('Instagram', 'instagram'),
        ('Tiktok', 'tiktok'),
    ]
    product_infos = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, default=1)
    social_category = models.CharField(max_length=10, choices=SOCIAL_CATEGORIES, default='Instagram')
    handle = models.CharField(max_length=30, validators=[validate_handle_input])
    
    def __str__(self):
        return self.handle
    
class SellerLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

    def __str__(self):
        return f"Latitude is {self.latitude} and Longitude is {self.longitude}"