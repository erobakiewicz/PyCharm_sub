from decimal import Decimal

from django.db import models

from subscriptions.constants import UserTypes, BillingType, SpecialOffers
from .constants import Countries


class Pricing(models.Model):
    SECOND_YEAR_DISCOUNT = Decimal('0.2')
    THIRD_YEAR_DISCOUNT = Decimal('0.25')

    offer_type = models.CharField(
        max_length=20,
        choices=SpecialOffers.Choices,
    )
    user_type = models.CharField(
        max_length=15,
        choices=UserTypes.Choices,
    )
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(
        max_length=50,
        choices=Countries.Choices,
        default=Countries.POLAND
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['offer_type', 'user_type'],
                name='unique pricing'
            )
        ]

    @property
    def price_yearly(self):
        return self.price_monthly * 10

    def get_tax_for_monthly(self):
        return self.price_monthly * Countries.TAXES.get(self.country)

    def get_tax_for_yearly(self):
        return self.price_yearly * Countries.TAXES.get(self.country)

    @property
    def get_total_price_monthly(self):
        return self.price_monthly + self.get_tax_for_monthly()

    @property
    def get_total_price_yearly(self):
        return self.price_yearly + self.get_tax_for_yearly()

    def second_year_yearly_price(self):
        return self.price_yearly - (self.price_yearly * self.SECOND_YEAR_DISCOUNT)

    def third_year_onwards_yearly_price(self):
        second_year = self.second_year_yearly_price()
        return second_year - (second_year * self.THIRD_YEAR_DISCOUNT)
