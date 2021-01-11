from django.test import TestCase, Client

from PyCharm_sub.factories import UserFactory, SubscriptionFactory

client = Client()


class SubscriptionModelTestCase(TestCase):

    def setup(self):
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
        assert sub.is_active == True
        assert sub.client.id == 1
        assert sub.client.first_name == 'fname0'

    def test_json_response(self):
        client = self.client
        sub = SubscriptionFactory()
        response = client.get(f'/subscription/{sub.id}/')
        assert response.status_code == 200
        print(type(response.json()))
        k = {'id': 1, 'sub_period': '2020-02-02', 'is_active': True, 'user_type':
            'individual', 'billing_type': 'yearly', 'special_offers': 'classroom_assistant', 'sub_quantity': 0,
                                    'us_tax': True, 'price': '20.00', 'client': 1}
        assert response.json() == k
