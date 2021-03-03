from django.urls import reverse
from products.test_base import get_product_dict
from customers.test_base import get_customer_dict


# EXAMPLE ORDER
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


def get_order_dict(client, order, response=None):
    '''Get dict from order'''
    if response is None:
        url = reverse('order-list')
        response = client.get(url, format='json')
    return {
        'id': str(order.id),
        'customer': get_customer_dict(order.customer, response),
        'items': [
            {
                'id': str(item.id),
                'product': get_product_dict(item.product, response),
                'price': str(item.price),
                'quantity': item.quantity

            } for item in order.items.all()
        ]
    }
