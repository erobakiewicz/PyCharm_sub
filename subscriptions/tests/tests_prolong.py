from datetime import timedelta
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from PyCharm_sub.factories import SubscriptionFactory, UserFactory
from subscriptions.constants import SpecialOffers, BillingType
from subscriptions.models import Subscription
from subscriptions.utils import check_is_active_when_outdated


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

    def test_deactivate_sub_after_valid_till(self):
        sub = SubscriptionFactory(
            client=self.user,
            is_active=True,
            billing_type=BillingType.MONTHLY,
            special_offers=SpecialOffers.NO_SPECIAL_OFFERS)

    def test_prolonged_before_end_date_valid_till(self):
        sub = SubscriptionFactory(
            client=self.user,
            billing_type='yearly',
            special_offers=SpecialOffers.NO_SPECIAL_OFFERS,
            date_created=timezone.now() + timedelta(weeks=4),
        )
        response = self.client.post(
            '/subscription/',
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get(
            'valid_till').strftime('%Y-%m-%d'), (
                sub.date_created + relativedelta(months=1)).strftime('%Y-%m-%d'))
        self.assertEqual(response.data.get('is_active'), True)
        sub_outdated = check_is_active_when_outdated(sub.id)
        # self.assertEqual(sub_outdated, True)
        # self.assertEqual(response.data.get('is_active'), False)

    def test_deactivate_no_response(self):
        two_years_ago = timezone.now() - relativedelta(years=2)
        print(two_years_ago, '<-- two years ago')
        sub = SubscriptionFactory(
            client=self.user,
            is_active=False,
            # date_created=two_years_ago,
            billing_type=BillingType.MONTHLY,
            special_offers=SpecialOffers.NO_SPECIAL_OFFERS
        )
        sub.valid = sub.date_created - relativedelta(years=2)
        print(sub.id, '<------ ID')
        print(sub.valid_from, '<------ DATE CREATED')
        sub_outdated = check_is_active_when_outdated(self.user)
        self.assertEqual(sub_outdated, False)
        print(self.user.subscription_set.all())
        print(sub.valid_till, "sub valid till")
