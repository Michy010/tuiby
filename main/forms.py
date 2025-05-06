from django import forms
from .models import ProductInfo, SocialInfo, SellerLocation

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ['product_name', 'product_descriptions']
        # widgets = {
        #     'product_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter product name'}),
        #     'product_descriptions': forms.Textarea(attrs={'class': 'input-field textarea', 'placeholder': 'Enter product description'}),
        #     'product_category': forms.Select(attrs={'class': 'input-field'}),
        # }
        product_category = forms.CharField(required=True)
    labels = {
        'product_name': 'Product Name',
        'product_descriptions': 'Product Description',
        'product_category': 'Category',
    }


class SocialInfoForm(forms.ModelForm):
    class Meta:
        model = SocialInfo
        fields = ['social_category', 'handle']
        widgets = {
            'social_category': forms.Select(attrs={'class': 'social-input-field'}),
            'handle': forms.TextInput(attrs={'class': 'social-input-field', 'placeholder': 'Enter your social handle eg @Msixoutfits'}),
        }

class SellerLocationForm(forms.ModelForm):
    class Meta:
        model = SellerLocation
        fields = ['latitude', 'longitude']