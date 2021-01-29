from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.db import models

from subscriptions.constants import UserTypes, BillingType, SpecialOffers


class Subscription(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    user_type = models.CharField(max_length=56, choices=UserTypes.Choices)
    billing_type = models.CharField(max_length=56, choices=BillingType.Choices)
    special_offers = models.CharField(max_length=128,
                                      choices=SpecialOffers.Choices,
                                      default=SpecialOffers.NO_SPECIAL_OFFERS)
    date_created = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()

    @property
    def valid_till(self):
        if self.billing_type == BillingType.MONTHLY:
            return self.date_created + relativedelta(months=1)
        else:
            return self.date_created + relativedelta(years=1)



