from rest_framework.test import APITestCase

from PyCharm_sub.factories import UserFactory, SubscriptionFactory
from orders.constants import OrderStatus
from orders.factories import OrderFactory
from orders.utils import check_if_sub_is_expensive, \
    check_if_sub_and_order_has_the_same_client, create_new_order_for_sub_id, set_order_status


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
        client_subscription_identity = check_if_sub_and_order_has_the_same_client(order, sub)
        self.assertEqual(client_subscription_identity, True)

    def test_create_order_for_sub_id(self):
        subscription = SubscriptionFactory(client=self.user)
        new_order = create_new_order_for_sub_id(subscription)
        self.assertEqual(new_order.subscription_id, subscription.id)

    def test_payment_status_declined(self):
        subscription = SubscriptionFactory(client=self.user)
        new_order = create_new_order_for_sub_id(subscription)
        status = OrderStatus.DECLINED
        payment_status = set_order_status(new_order, status)
        self.assertEqual(payment_status, OrderStatus.DECLINED)

    def test_payment_status_success(self):
        subscription = SubscriptionFactory(client=self.user)
        new_order = create_new_order_for_sub_id(subscription)
        status = OrderStatus.PAID
        print(new_order.order_status, "Before")
        payment_status = set_order_status(new_order, status)
        self.assertEqual(payment_status, OrderStatus.PAID)
        print(new_order.order_status, "After")

    def test_calculate_order_expnesive(self):
        """Sprawdź czy jak kupisz drogą subskrycpjcę to czy jest droga"""
        expensive = 300
        order = OrderFactory(price=200)
        expensive_sub = check_if_sub_is_expensive(order, expensive)
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
