from datetime import datetime
from datetime import timedelta
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from PyCharm_sub.factories import SubscriptionFactory, UserFactory
from subscriptions.constants import SpecialOffers, BillingType
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
        print(response.data.get('valid_from'))
        valid_from_date = datetime.strptime(response.data.get('valid_from'), '%Y-%m-%dT%H:%M:%S.%fZ').date()
        self.assertEqual(valid_from_date, sub.valid_till.date())

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
    def test_send_email_after_successful_prolog(self, mocked_send_notification_mail):
        SubscriptionFactory(client=self.user, special_offers=SpecialOffers.NO_SPECIAL_OFFERS)
        response = self.client.post(
            '/subscription/',
        )

        self.assertEqual(response.status_code, 201)
        mocked_send_notification_mail.assert_called_once()

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
        valid_from_date = datetime.strptime(response.data.get('valid_from'), '%Y-%m-%dT%H:%M:%S.%fZ').date()
        self.assertEqual(valid_from_date, sub.valid_till.date())

    def test_deactivate_sub_after_valid_till(self):
        sub = SubscriptionFactory(
            client=self.user,
            is_active=True,
            billing_type=BillingType.MONTHLY,
            special_offers=SpecialOffers.NO_SPECIAL_OFFERS,
        )

    def test_prolonged_before_end_date_valid_till(self):
        """
        Stara subskrypcja jest miesięczna, zaczyna obowiązywać dzisiaj,
        więc nowa powinna zacząć działać dopiero za miesiąc.
        """
        month_later = timezone.now() + relativedelta(months=1)
        old_sub = SubscriptionFactory(
            client=self.user,
            billing_type=BillingType.MONTHLY,
            special_offers=SpecialOffers.NO_SPECIAL_OFFERS,
            valid_from=timezone.now(),
        )
        response = self.client.post(
            '/subscription/',
        )
        self.assertEqual(response.status_code, 201)
        new_sub = Subscription.objects.filter(client=self.user).order_by('-date_created').first()
        self.assertNotEqual(new_sub.id, old_sub.id)
        self.assertEqual(new_sub.valid_from.date(), month_later.date())
