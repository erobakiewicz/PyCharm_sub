from rest_framework.test import APITestCase

from PyCharm_sub.factories import UserFactory, SubscriptionFactory
from orders.factories import OrderFactory
from orders.utils import check_if_subscription_is_ordered, check_if_sub_is_expensive


class NewOrderTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.subscription = SubscriptionFactory()
        self.order = OrderFactory()

    def test_simple_order(self):
        """Endpoint przyjmuje id nowej subskrypcji, tworzy nowy order"""
        # sprawdź czy subskrypcaj i order mają tego samego clienta
        sub = SubscriptionFactory(client=self.user)
        OrderFactory(subscription=sub)
        print(self.order.email, '<-------------')
        existing_order = check_if_subscription_is_ordered(self.user)
        print(existing_order)
        self.assertEqual(existing_order, True)

    def test_calculate_order_expnesive(self):
        """Sprawdź czy jak kupisz drogą subskrycpjcę to czy jest droga"""
        expensive = 300
        order = OrderFactory(price=200)
        expensive_sub = check_if_sub_is_expensive(order,expensive)
        self.assertEqual(expensive_sub, True)

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
