from django.db import models
from decimal import Decimal
from django.conf import settings
from store.models import Product
from django_countries.fields import CountryField

import uuid


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='order_user'
    )
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    country = CountryField()
    state = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    email = models.EmailField()
    post_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200)
    order_number = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.billing_status)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
