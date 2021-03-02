import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from customers.models import Customer
from products.models import Product

from .models import Order, Item


def to_dict(input_ordered_dict):
    return json.loads(json.dumps(input_ordered_dict))


ORDERS = [
    {
        'customer': 1,
        'items': [
            {
                'product': 1,
                'price': 550000,
                'quantity': 5
            },
            {
                'product': 2,
                'price': 60000,
                'quantity': 3
            }

        ]
    },
    {
        'customer': 1,
        'items': [
            {
                'product': 1,
                'price': 550000,
                'quantity': 5
            }

        ]
    }
]


def get_photo_url_or_null(response, photo):
    if photo is None:
        return None
    if photo:
        request = response.wsgi_request
        return f'{request.scheme}://{request.get_host()}{photo.url}'
    return None
    

class ProductTest(TestCase):

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
            name='MUDAR DEPOIS',
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
        # response = self.client.post(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_detail_view(self):
        url = reverse('order-detail', args=[self.order1.id])
        response = self.client.get(url)
        order1 = {
            'id': str(self.order1.id),
            'customer': {
                'id': self.order1.customer.id,
                'name': self.order1.customer.name,
                'photo': get_photo_url_or_null(response, self.order1.customer.photo)
            },
            'items': [
                {
                    'id': str(item.id),
                    'product': {
                        'id': item.product.id,
                        'name': item.product.name,
                        'price': str(item.product.price),
                        'multiple': item.product.multiple,
                        'photo': get_photo_url_or_null(response, item.product.photo)
                    },
                    'price': str(item.price),
                    'quantity': item.quantity

                } for item in self.order1.items.all()
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(to_dict(response.data), to_dict(order1))
        order1['customer'] = self.customer2.id
        order1['items'] = [
            {
                'product': 2,
                'price': 60000,
                'quantity': 3
            }

        ]
        print(to_dict(order1))
        response = self.client.put(url, to_dict(order1), content_type='application/json')
        print('response.data [ATUALIZADO]')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_view(self):
        url = reverse('order-list')
        client = APIClient()
        print(ORDERS[0])
        response = client.post(url, ORDERS[0], format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)







    '''def test_other_methods_detail_view(self):
        url = reverse('order-detail', args=['1'])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    '''
