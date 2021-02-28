from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Customer

NAME_TEST = 'Darth Vader'
NAME_TEST_2 = 'Obi-Wan Kenobi'


class CustomerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.customer1 = Customer.objects.create(
            name=NAME_TEST,
            photo='image.png'
        )
        cls.customer2 = Customer.objects.create(
            name=NAME_TEST_2,
            photo='image.png'
        )

    def test_str(self):
        self.assertEqual(str(self.customer1), NAME_TEST)
        self.assertEqual(str(self.customer2), NAME_TEST_2)

    def test_get_list_view(self):
        url = reverse('customer-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_other_methods_list_view(self):
        url = reverse('customer-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_view(self):
        url = reverse('customer-detail', args=['1'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], NAME_TEST)

    def test_other_methods_detail_view(self):
        url = reverse('customer-detail', args=['1'])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
