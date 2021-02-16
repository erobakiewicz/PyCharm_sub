from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from subscriptions.constants import UserTypes, BillingType, SpecialOffers


class Subscription(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    is_active = models.BooleanField()
    user_type = models.CharField(max_length=56, choices=UserTypes.Choices)
    billing_type = models.CharField(max_length=56, choices=BillingType.Choices)
    special_offers = models.CharField(
        max_length=128,
        choices=SpecialOffers.Choices,
        default=SpecialOffers.NO_SPECIAL_OFFERS,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.client} - {self.billing_type}'

    @property
    def valid_till(self):
        if self.billing_type == BillingType.MONTHLY:
            return self.valid_from + relativedelta(months=1)
        else:
            return self.valid_from + relativedelta(years=1)

