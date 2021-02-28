from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=500)
    photo = models.ImageField(upload_to="customers", null=True, blank=True)

    def __str__(self):
        return self.name
