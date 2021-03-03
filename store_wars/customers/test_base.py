'''Base for tests'''
from utils.url_helpers import get_photo_url_or_null


def get_customer_dict(customer, response):
    return {
        'id': customer.id,
        'name': customer.name,
        'photo': get_photo_url_or_null(response, customer.photo)
    }
