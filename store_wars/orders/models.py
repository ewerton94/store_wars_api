import uuid

from django.db import models

from customers.models import Customer
from products.models import Product

PROFITABILITY = (
    ('excellent', 'Excellent'),
    ('good', 'Good'),
    ('bad', 'Bad'),
)


def get_multiple_situation(product=None, item=None, product_id=None):
    if product_id is not None:
        product = Product.objects.get(id=product_id).multiple
    if product is not None:
        if item % product == 0:
            return True
    return False


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.name


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=15)
    profitability = models.CharField(max_length=50, choices=PROFITABILITY, blank=True, null=True)

    def __str__(self):
        return f'Pedido de {self.order.customer.name} - {self.quantity} {self.product.name} a {self.price}'

    @property
    def multiple_satisfies(self):
        return get_multiple_situation(self.product.multiple, self.quantity)

    def calculate_profitability(self):
        product_price = float(self.product.price)
        item_price = float(self.price)
        if round(item_price, 2) > round(product_price, 2):
            return 'excellent'
        elif round(product_price * 0.9, 2) <= round(item_price, 2) <= round(product_price, 2):
            return 'good'
        else:
            return 'bad'

    def save(self, *args, **kwargs):
        if self.profitability is None:
            self.profitability = self.calculate_profitability()
        super().save(*args, **kwargs)
