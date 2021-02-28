from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Product

NAME_TEST = 'Millenium Falcon'
NAME_TEST_2 = 'X-Wing'


class ProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product1 = Product.objects.create(
            name=NAME_TEST,
            photo='image.png',
            price=550000
        )
        cls.product2 = Product.objects.create(
            name=NAME_TEST_2,
            price=60000,
            multiple=5
        )

    def test_str(self):
        self.assertEqual(str(self.product1), NAME_TEST)
        self.assertEqual(str(self.product2), NAME_TEST_2)

    def test_get_list_view(self):
        url = reverse('product-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_other_methods_list_view(self):
        url = reverse('product-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_view(self):
        url = reverse('product-detail', args=['1'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], NAME_TEST)

    def test_other_methods_detail_view(self):
        url = reverse('product-detail', args=['1'])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
