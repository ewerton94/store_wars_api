'''Base for tests'''
from utils.url_helpers import get_photo_url_or_null


def get_product_dict(product, response):
    '''Get dict from product'''
    return {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'multiple': product.multiple,
        'photo': get_photo_url_or_null(response, product.photo)
    }
