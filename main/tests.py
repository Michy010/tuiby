from django.test import TestCase, Client
from . models import ProductInfo
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='Mary', email='marykassim@gmail.com', password='MaryM123')
        self.product = ProductInfo.objects.create(product_name='Simu', user=self.user,
                                                  product_descriptions='Iphone 11', 
                                                  product_category='electronics')
    def test_products_creation(self):
        response = self.client.get(reverse('main:add_product'))
        self.assertEqual(response.status_code, 302)