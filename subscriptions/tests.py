from datetime import timedelta

from django.test import TestCase, Client
from django.utils import timezone
from rest_framework.test import APIClient

from PyCharm_sub.factories import UserFactory, SubscriptionFactory
from subscriptions.utils import check_if_user_has_valid_subscription

client = Client()


class SubscriptionModelTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.subscription = SubscriptionFactory()
        self.client = Client()

    def test_user(self):
        user = UserFactory()
        assert user.username == 'username0'
        assert user.first_name == 'fname0'
        assert user.last_name == 'lname0'

    def test_subscription(self):
        sub = SubscriptionFactory()
        assert sub.price == 20.0
        assert sub.is_active == False
        assert sub.client.id == 1
        assert sub.client.first_name == 'fname0'

    def test_active_subscription(self):
        SubscriptionFactory(is_active=True, client=self.user, sub_period=timezone.now() + timedelta(weeks=1))
        has_valid_sub = check_if_user_has_valid_subscription(self.user)
        self.assertEqual(has_valid_sub, True)

    def test_inactive_subscription(self):
        SubscriptionFactory(is_active=False, client=self.user)
        has_valid_sub = check_if_user_has_valid_subscription(self.user)
        self.assertEqual(has_valid_sub, False)

    def test_inactive_subscription_None(self):
        SubscriptionFactory(client=self.user, is_active=True)
        SubscriptionFactory(client=self.user, is_active=False)
        has_valid_sub = check_if_user_has_valid_subscription(self.user)
        self.assertEqual(has_valid_sub, True)