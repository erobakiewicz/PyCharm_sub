from django.db import models

from orders.constants import OrderStatus
from subscriptions.models import Subscription


class Order(models.Model):
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
        related_name='order',
    )
    order_status = models.CharField(
        max_length=50,
        choices=OrderStatus.Choices,
        default=OrderStatus.IN_PROGRESS,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # def get_email(self):
    #     if self.email is None:
    #         self.email = Subscription.objects.get(client__email=...)
