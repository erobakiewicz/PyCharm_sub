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
        if not self.prolong_validation():
            raise ProlongingError
        # 2. do the thing
        self.create_new_prolonged_sub()
        # 3. send some notifications or smth
        self.send_notification_mail()
        return

    def prolong_validation(self):
        if self.subscription.special_offers == SpecialOffers.STUDENT:
            self.errors.update(
                {
                    'error1': 'Nie możesz przedłużyć subskrypcji studenckiej. Zapłać normalnie hajs kutafonie.'
                }
            )
            return False
        return True


    def prolong_date_validation(self):
        sub_query = Subscription.objects.all().order_by('-date_created')[1]
        last_sub_valid_till = sub_query.valid_till
        print(last_sub_valid_till,"last_sub_valid_till")
        if last_sub_valid_till < self.subscription.date_created:
            self.subscription.date_created = last_sub_valid_till
            print(self.subscription.date_created, 'date created')
            return self.subscription.date_created
        else:
            return self.subscription.date_created

    def create_new_prolonged_sub(self):
        obj = Subscription.objects.create(
            client=self.subscription.client,
            date_created=self.subscription.date_created,
            is_active=True,
            user_type=self.subscription.user_type,
            billing_type=self.subscription.billing_type,
            special_offers=self.subscription.special_offers,
        )
        self.prolong_date_validation()
        if obj.billing_type == BillingType.MONTHLY:
            self.new_sub = SubscriptionSerializer(obj).data
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
