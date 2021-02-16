from decimal import Decimal

from django.test import TestCase

from pricing.factories import PricingFactory
from pricing.models import Pricing


class YearlyPriceTest(TestCase):

    def setUp(self):
        self.pricing = PricingFactory(price_monthly=Decimal('50.00'))

    def test_second_year_price(self):
        '''
        Testing second_year_yearly_price method from Pricing model
        Checking if second year discount is equal to SECOND_YEAR_DISCOUNT amount in Pricing model
        discount from the original price
        Checking if price from the first year minus discount is equal to secon year price
        '''
        first_year_price = self.pricing.price_yearly
        second_year_discount = first_year_price * Pricing.SECOND_YEAR_DISCOUNT
        second_year_price = self.pricing.second_year_yearly_price()

        self.assertEqual(first_year_price - second_year_discount, second_year_price)
        self.assertEqual(second_year_discount, Decimal('100.00'))
        self.assertNotEqual(first_year_price, second_year_price)
        self.assertGreater(first_year_price, second_year_price)

    def test_third_year_price(self):
        '''
        Testing third_year_onwards_yearly_price method from Pricing model
        Checking if third year discount is equal to THIRD_YEAR_DISCOUNT amount in Pricing model
        Checking if third year price is equal to second year price minus discount
        '''
        first_year_price = self.pricing.price_yearly
        second_year_price = self.pricing.second_year_yearly_price()
        third_year_price = self.pricing.third_year_onwards_yearly_price()
        third_year_discount = second_year_price * Pricing.THIRD_YEAR_DISCOUNT

        self.assertEqual(third_year_discount, Decimal('100.00'))
        self.assertEqual(second_year_price - third_year_discount, third_year_price)
        self.assertNotEquals(first_year_price, second_year_price, third_year_price)
        self.assertGreater(first_year_price, second_year_price, third_year_price)
