from django.contrib.auth.models import User
from django.test import TestCase

from PyCharm_sub.factories import UserFactory, SubscriptionFactory

class SubscriptionModelTestCase(TestCase):
    def setup(self):
        self.user = UserFactory()
        self.subscription = SubscriptionFactory()


    def test_user(self):
        user = UserFactory()
        assert user.username == 'username0'
        assert user.first_name == 'fname0'
        assert user.last_name == 'lname0'


    def test_subscription(self):
        sub = SubscriptionFactory()
        assert sub.price == 20.0

