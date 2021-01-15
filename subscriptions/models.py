from django.contrib.auth.models import User
from django.db import models

from subscriptions.constants import UserTypes, BillingType, SpecialOffers


class Subscription(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_period = models.DateField()
    is_active = models.BooleanField()
    user_type = models.CharField(max_length=56, choices=UserTypes.Choices)
    billing_type = models.CharField(max_length=56, choices=BillingType.Choices)
    special_offers = models.CharField(max_length=128,choices=SpecialOffers.Choices)
    sub_quantity = models.PositiveIntegerField(default=1)
    us_tax = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# class Order(models.Model):
#     subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
#     subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
#     order_status = models.CharField(choices=OrderStatus.Choices)
#     country = models.CharField(choices=Countries.Choices)
#     tax = models.DecimalField(max_digits=10, decimal_places=2)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     email = models.EmailField(default=subscription.client.email)
