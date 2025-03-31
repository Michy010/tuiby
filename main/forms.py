from django import forms
from .models import ProductInfo

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ['product_name', 'product_descriptions', 'product_category']
        # widgets = {
        #     'product_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter product name'}),
        #     'product_descriptions': forms.Textarea(attrs={'class': 'input-field textarea', 'placeholder': 'Enter product description'}),
        #     'product_category': forms.Select(attrs={'class': 'input-field'}),
        # }
    labels = {
        'product_name': 'Product Name',
        'product_descriptions': 'Product Description',
        'product_category': 'Category',
    }
