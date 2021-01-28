from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from PyCharm_sub.factories import SubscriptionFactory, UserFactory
from subscriptions.constants import SpecialOffers
from subscriptions.models import Subscription


class SubscriptionProlongingTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_successful_prolong(self):
        sub = SubscriptionFactory(client=self.user, special_offers=SpecialOffers.NO_SPECIAL_OFFERS)
        subscription_count_before = Subscription.objects.count()
        response = self.client.post(
            '/subscription/',
        )
        subscription_count_after = Subscription.objects.count()

        self.assertEqual(response.status_code, 201)

        self.assertEqual(subscription_count_before + 1, subscription_count_after)

        self.assertEqual(response.data['date_created'][0:19], sub.date_created.strftime("%Y-%m-%dT%H:%M:%S"))
        self.assertEqual(response.data.get('user_type'), sub.user_type)
        self.assertEqual(response.data.get('billing_type'), sub.billing_type)
        self.assertEqual(response.data.get('special_offers'), sub.special_offers)
        self.assertEqual(response.data.get('valid_till').strftime("%Y-%m-%dT%H:%M:%S"),
                         sub.valid_till.strftime("%Y-%m-%dT%H:%M:%S"))

    def test_unsuccessful_prolong_when_student(self):
        SubscriptionFactory(client=self.user, special_offers=SpecialOffers.STUDENT)
        response = self.client.post(
            '/subscription/',
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data.get('error1'),
            'Nie możesz przedłużyć subskrypcji studenckiej. Zapłać normalnie hajs kutafonie.',
        )

    def test_unsuccessful_prolong_does_not_have_subscription(self):
        response = self.client.post(
            '/subscription/',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(None, response.data.get('date_created'))

    @patch('subscriptions.services.prolong.ProlongSubscription.send_notification_mail')
    def test_send_email_after_successful_prolog(self, mock):
        SubscriptionFactory(client=self.user, special_offers=SpecialOffers.NO_SPECIAL_OFFERS)
        response = self.client.post(
            '/subscription/',
        )

        self.assertEqual(response.status_code, 201)
        mock.assert_called_once()

    def test_prolonged_valid_till(self):
        sub = SubscriptionFactory(
            client=self.user,
            billing_type='yearly',
            special_offers=SpecialOffers.NO_SPECIAL_OFFERS
        )
        response = self.client.post(
            '/subscription/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("valid_till").strftime("%Y-%m-%dT%H:%M:%S"),
                         (sub.valid_till).strftime("%Y-%m-%dT%H:%M:%S"))
