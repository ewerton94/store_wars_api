from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=500)
    photo = models.ImageField(upload_to="products", null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15)
    multiple = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.name
