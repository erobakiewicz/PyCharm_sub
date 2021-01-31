from rest_framework.test import APITestCase

from PyCharm_sub.factories import UserFactory, SubscriptionFactory
from orders.factories import OrderFactory
from orders.utils import check_if_sub_and_order_has_the_same_client


class NewOrderTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.subscription = SubscriptionFactory()
        self.order = OrderFactory()

    def test_simple_order(self):
        """Endpoint przyjmuje id nowej subskrypcji, tworzy nowy order"""
        # sprawdź czy subskrypcaj i order mają tego samego clienta
        sub = SubscriptionFactory(client=self.user)
        order = OrderFactory(subscription=sub)
        client_id = check_if_sub_and_order_has_the_same_client(order, sub)
        self.assertEqual(client_id, True)

    def test_calculate_order_expensive(self):
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
