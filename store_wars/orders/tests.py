import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from customers.models import Customer
from products.models import Product

from .models import Order, Item
from .test_base import get_order_dict, ORDERS


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))


class OrderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product_without_multiple, created = Product.objects.get_or_create(
            name='Millenium Falcon',
            photo='image.png',
            price=550000
        )
        cls.product_with_multiple, created = Product.objects.get_or_create(
            name='X-Wing',
            price=60000,
            multiple=2
        )
        cls.customer, created = Customer.objects.get_or_create(
            name='Darth Vader',
            photo='image.png'
        )
        cls.customer2, created = Customer.objects.get_or_create(
            name='Obi-Wan Kenobi',
            photo='image.png'
        )
        cls.order1 = Order.objects.create(customer=cls.customer)
        cls.order2 = Order.objects.create(customer=cls.customer)
        cls.item1 = Item.objects.create(
            order=cls.order1,
            product=cls.product_without_multiple,
            price=550000,
            quantity=1
        )
        cls.item2 = Item.objects.create(
            order=cls.order1,
            product=cls.product_with_multiple,
            price=550000,
            quantity=2
        )
        cls.item3 = Item.objects.create(
            order=cls.order1,
            product=cls.product_without_multiple,
            price=55000.01,
            quantity=3
        )
        cls.order1_dict = get_order_dict(APIClient(), cls.order1)

    def test_str(self):
        self.assertEqual(str(self.order1), self.order1.customer.name)
        self.assertEqual(str(self.order2), self.order2.customer.name)

    def test_get_list_view(self):
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_other_methods_list_view(self):
        url = reverse('order-list')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_view(self):
        url = reverse('order-detail', args=[self.order1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(to_dict(response.data), to_dict(self.order1_dict))

    def test_update_view(self):
        url = reverse('order-detail', args=[self.order1.id])
        self.order1_dict['customer'] = self.customer2.id
        self.order1_dict['items'] = [
            {
                'product': 2,
                'price': 60000,
                'quantity': 3
            }

        ]
        response = self.client.put(url, to_dict(self.order1_dict), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_view(self):
        url = reverse('order-list')
        client = APIClient()
        response = client.post(url, ORDERS[0], format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
