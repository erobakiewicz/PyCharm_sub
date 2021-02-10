from django.core.mail import send_mail
from django.utils import timezone

from subscriptions.constants import SpecialOffers
from subscriptions.errors import ProlongingError
from subscriptions.models import Subscription


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
        obj = Subscription.objects.create(
            client=self.subscription.client,
            date_created=self.subscription.date_created,))

    def send_notification_mail(self):
        prolonged_subscription = self.new_sub
        subject = f'Your Pycharm subscription {prolonged_subscription.id} is prolonged.'
        message = f'Dear {prolonged_subscription.client.first_name} {prolonged_subscription.client.last_name},' \
                  f'Your {prolonged_subscription.billing_type} subscription has been prolonged untill' \
                  f' {prolonged_subscription.valid_till.strftime("%Y-%m-%d")}.'
        mail_sent = send_mail(subject,
                              message,
                              "admin@pycharmshop.com",
                              {prolonged_subscription.client.email})
        return mail_sent
