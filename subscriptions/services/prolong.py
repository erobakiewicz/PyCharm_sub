from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

from subscriptions.constants import SpecialOffers, BillingType
from subscriptions.errors import ProlongingError
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class ProlongSubscription:
    errors = {}
    new_sub = None

    def __init__(self, subscription):
        self.subscription = subscription
        self.user = self.subscription.client

    def prolong(self):
        # 1. check it its possible
        if not self.all_good():
            raise ProlongingError
        # 2. do the thing
        self.create_new_prolonged_sub()
        # 3. send some notifications or smth
        self.send_notification_mail()
        return

    def all_good(self):
        if self.subscription.special_offers == SpecialOffers.STUDENT:
            self.errors.update(
                {
                    'error1': 'Nie możesz przedłużyć subskrypcji studenckiej. Zapłać normalnie hajs kutafonie.'
                }
            )
            return False
        return True

    def create_new_prolonged_sub(self):
        last_sub_valid_till = Subscription.objects.filter(client=self.user).last()
        print(last_sub_valid_till.valid_till)
        obj = Subscription.objects.create(
            client=self.subscription.client,
            date_created=self.subscription.date_created,
            is_active=True,
            user_type=self.subscription.user_type,
            billing_type=self.subscription.billing_type,
            special_offers=self.subscription.special_offers,
        )
        if obj.billing_type == BillingType.MONTHLY:
            a = last_sub_valid_till.valid_till + relativedelta(months=1)
            self.new_sub = SubscriptionSerializer(obj).data
            print(obj.date_created)
            print(obj.valid_till)

            return self.new_sub
        else:
            obj.date_created + relativedelta(years=1)
            self.new_sub = SubscriptionSerializer(obj).data
            return self.new_sub


    def send_notification_mail(self):
        # send_mail(
        #     subject='eeeeeee',
        #     message='Masz nową subskrypcję PyCharma'
        # )
        pass
