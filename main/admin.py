from django.contrib import admin
from . models import SellerLocation, ProductInfo, SocialInfo
# Register your models here.
admin.site.register(SocialInfo)
admin.site.register(SellerLocation)
admin.site.register(ProductInfo)