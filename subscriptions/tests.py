from django.contrib.auth.models import User
from django.test import TestCase

from PyCharm_sub.factories import UserFactory, SubscriptionFactory

class SubscriptionModelTestCase(TestCase):
    def setup(self):
        self.user = UserFactory()
        self.subscription = SubscriptionFactory()


    def test_user(self, client):
        user = UserFactory()
        subscription = SubscriptionFactory()
        response = client.post('/subscription', subscription)
        assert User.objects.all().count() != 0