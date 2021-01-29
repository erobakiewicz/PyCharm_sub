from dateutil.relativedelta import relativedelta
from django.utils import timezone

from subscriptions.constants import SpecialOffers, BillingType
from subscriptions.errors import ProlongingError
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class ProlongSubscription:
    errors = {}
    new_sub = None

    def __init__(self, subscription):
        self.old_subscription = subscription
        self.user = self.old_subscription.client

    def prolong(self):
        # 1. check it its possible
        if not self.prolong_validation():
            raise ProlongingError
        # 2. do the thing
        self.create_new_prolonged_sub()
        # 3. send some notifications or smth
        self.send_notification_mail()
        return

    def prolong_validation(self):
        if self.old_subscription.special_offers == SpecialOffers.STUDENT:
            self.errors.update(
                {
                    'error1': 'Nie możesz przedłużyć subskrypcji studenckiej. Zapłać normalnie hajs kutafonie.'
                }
            )
            return False
        return True

    def get_valid_from(self):
        if timezone.now() < self.old_subscription.valid_till:
            return self.old_subscription.valid_till
        else:
            return timezone.now()

    def create_new_prolonged_sub(self):
        self.new_sub = Subscription.objects.create(
            client=self.old_subscription.client,
            is_active=True,
            user_type=self.old_subscription.user_type,
            billing_type=self.old_subscription.billing_type,
            special_offers=self.old_subscription.special_offers,
            valid_from=self.get_valid_from()
        )

    def send_notification_mail(self):
        # send_mail(
        #     subject='eeeeeee',
        #     message='Masz nową subskrypcję PyCharma'
        # )
        pass
