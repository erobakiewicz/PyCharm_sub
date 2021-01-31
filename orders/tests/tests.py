from rest_framework.test import APITestCase

from PyCharm_sub.factories import UserFactory, SubscriptionFactory
from orders.factories import OrderFactory
from orders.utils import check_if_subscription_is_ordered


class NewOrderTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.subscription = SubscriptionFactory()
        self.order = OrderFactory()

    def test_simple_order(self):
        """Endpoint przyjmuje id nowej subskrypcji, tworzy nowy order"""
        # sprawdź czy subskrypcaj i order mają tego samego clienta
        OrderFactory(subscription=self.subscription)
        print(self.order.email, '<-------------')
        existing_order = check_if_subscription_is_ordered(self.user)
        self.assertEqual(existing_order, True)

    def test_calculate_orde_expnesive(self):
        """Sprawdź czy jak kupisz drogą subskrycpjcę to czy jest droga"""
        pass

    def test_calculate_order_cheap(self):
        """Sprawdź czy jak kupisz tanią subskrycpjcę to czy jest tania"""
        pass

    def test_payment_successful(self):
        """Udana płatność. Przyjmuje id orderu i zmienia jego status,
        oraz status pokrewenj subskrypcji"""
        pass

    def test_payment_failed(self):
        """coś wymyślcie"""
        pass

    def test_email_client_after_successful_payment(self):
        """skorzystaj z mocka"""
        pass
