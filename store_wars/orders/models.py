import uuid

from django.db import models

from customers.models import Customer
from products.models import Product

PROFITABILITY = (
    ('excellent', 'Excellent'),
    ('good', 'Good'),
    ('bad', 'Bad'),
)


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
    profitability = models.CharField(max_length=50, choices=PROFITABILITY)

    def __str__(self):
        return f'Pedido de {self.order.customer.name} - {self.quantity} {self.product.name} a {self.price}'

    def get_profitability(self):
        if round(self.price, 2) > round(self.product.price, 2):
            return 'excellent'
        elif round(self.product.price * 0.9, 2) <= round(self.price, 2) <= round(self.product.price, 2):
            return 'good'
        else:
            return 'bad'

    def save(self, *args, **kwargs):
        if self.profitability is None:
            self.profitability = self.get_profitability()
        super(Item, self).save(*args, **kwargs)