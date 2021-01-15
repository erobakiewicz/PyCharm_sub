from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from unittest.mock import patch

from PyCharm_sub.factories import UserFactory, SubscriptionFactory
from subscriptions.constants import SpecialOffers
from subscriptions.models import Subscription
from subscriptions.utils import check_if_user_has_valid_subscription, check_if_user_has_invalid_subscription, \
    check_if_user_has_monthly_subscription, check_if_user_has_yearly_subscription, check_if_user_has_valid_type, \
    check_if_subscription_was_added_to_user, check_if_valid_monthly_subscription_is_added, \
    check_all_users_with_vaild_sub, check_all_user_subscriptions, check_user_has_valid_billing_type

client = Client()


class SubscriptionModelTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()

        self.subscription = SubscriptionFactory()
        self.client = Client()

    def test_user_has_no_subscription(self):
        has_sub = check_if_user_has_valid_subscription(self.user)
        print(self.user.subscription_set.exists())
        self.assertEqual(has_sub, False)

    def test_active_subscription(self):
        sub0 = SubscriptionFactory(is_active=True, client=self.user, sub_period=timezone.now() + timedelta(weeks=1))
        has_valid_sub = check_if_user_has_valid_subscription(self.user)
        print(sub0.sub_period)
        self.assertEqual(has_valid_sub, True)

    def test_inactive_subscription(self):
        sub = SubscriptionFactory(is_active=False, client=self.user)
        has_valid_sub = check_if_user_has_valid_subscription(self.user)
        print(sub.sub_period)
        self.assertEqual(has_valid_sub, False)

    def test_inactive_while_active(self):
        SubscriptionFactory(client=self.user, is_active=True)
        SubscriptionFactory(client=self.user, is_active=False)
        has_valid_sub = check_if_user_has_valid_subscription(self.user)
        self.assertEqual(has_valid_sub, True)

    def test_active_subscription_monthly(self):
        sub = SubscriptionFactory(is_active=True, client=self.user, sub_period=timezone.now() + timedelta(weeks=4),
                                  billing_type='monthly')
        has_monthly_sub = check_if_valid_monthly_subscription_is_added(self.user)
        print(sub.sub_period)
        self.assertEqual(has_monthly_sub, True)

    def test_subscription_added_to_user(self):
        SubscriptionFactory(client=self.user)
        sub_added = check_if_subscription_was_added_to_user(self.user)
        self.assertEqual(sub_added, True)

    def test_user_type(self):
        SubscriptionFactory(user_type="individual", client=self.user)
        has_valid_type = check_if_user_has_valid_type(self.user)
        self.assertEqual(has_valid_type, True)

    def test_user_wrong_type(self):
        SubscriptionFactory(user_type="random", client=self.user)
        has_valid_type = check_if_user_has_valid_type(self.user)
        self.assertEqual(has_valid_type, False)

    def test_user_type_choice(self):
        sub = SubscriptionFactory(client=self.user)
        has_valid_type = check_if_user_has_valid_type(self.user)
        print(sub.user_type)
        self.assertEqual(has_valid_type, True)

    def test_inactive_sub_period_subscription(self):
        SubscriptionFactory(client=self.user, is_active=False, sub_period=timezone.now() - timedelta(weeks=4))
        has_valid_sub = check_if_user_has_invalid_subscription(self.user)
        self.assertEqual(has_valid_sub, True)

    def test_if_user_has_monthly_sub(self):
        SubscriptionFactory(client=self.user, is_active=True, billing_type='monthly')
        has_monthly_sub = check_if_user_has_monthly_subscription(self.user)
        self.assertEqual(has_monthly_sub, True)

    def test_if_user_has_yearly_sub(self):
        SubscriptionFactory(client=self.user, is_active=True, billing_type='yearly')
        has_yearly_sub = check_if_user_has_yearly_subscription(self.user)
        self.assertEqual(has_yearly_sub, True)

    def test_if_users_have_valid_billing_type(self):
        SubscriptionFactory(client=self.user, is_active=True, billing_type='monthly')
        SubscriptionFactory(client=self.user1, is_active=True, billing_type='yearly')
        user_has_valid_billing_type = check_user_has_valid_billing_type(self.user)
        user_has_valid_billing_type1 = check_user_has_valid_billing_type(self.user1)
        print(user_has_valid_billing_type)
        print(user_has_valid_billing_type1)
        self.assertEqual(user_has_valid_billing_type, True)
        self.assertEqual(user_has_valid_billing_type1, True)


class QueryAllTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user1 = UserFactory()
        self.subscription = SubscriptionFactory(is_active=True, client=self.user)
        self.subscription = SubscriptionFactory(is_active=False, client=self.user1)

    def test_show_all_users_with_valid_subscription(self):
        print(User.objects.all().values('subscription__id'))
        print(User.objects.all().values('username'))
        all_users_with_valid_subscription = check_all_users_with_vaild_sub()
        print(all_users_with_valid_subscription)
        self.assertGreater(all_users_with_valid_subscription, 0)

    def test_show_all_subscriptions_of_a_user(self):
        all_user_sub = check_all_user_subscriptions(self.user)
        print(all_user_sub)
        self.assertTrue(all_user_sub, Subscription.objects.filter(client=self.user))


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

        self.assertEqual(response.data.get('sub_period'), sub.sub_period)
        self.assertEqual(response.data.get('user_type'), sub.user_type)
        self.assertEqual(response.data.get('billing_type'), sub.billing_type)
        self.assertEqual(response.data.get('special_offers'), sub.special_offers)
        self.assertEqual(response.data.get('sub_quantity'), sub.sub_quantity)
        self.assertEqual(response.data.get('us_tax'), sub.us_tax)
        self.assertEqual(response.data.get('price'), str(sub.price))

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
        self.assertIn('This field is required.', response.data.get('sub_period'))

    @patch('subscriptions.services.prolong.ProlongSubscription.send_notification_mail')
    def test_send_email_after_successful_prolog(self, mock):
        SubscriptionFactory(client=self.user, special_offers=SpecialOffers.NO_SPECIAL_OFFERS)
        response = self.client.post(
            '/subscription/',
        )

        self.assertEqual(response.status_code, 201)
        mock.assert_called_once()
