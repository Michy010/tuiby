from django.contrib import admin
from . models import SellerLocation, ProductInfo, SocialInfo, BusinessProfile, Statistic
# Register your models here.
admin.site.register(SocialInfo)
admin.site.register(SellerLocation)
admin.site.register(ProductInfo)
admin.site.register(BusinessProfile)
admin.site.register(Statistic)