from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.utils import timezone

from subscriptions.models import Subscription

from subscriptions.constants import BillingType, UserTypes, SpecialOffers


def check_if_user_has_valid_subscription(user):
    return user.subscriptions.filter(
        is_active=True,
        date_created__gte=timezone.now().date()
    ).exists()


def check_if_subscription_was_added_to_user(user):
    clients_subscriptions = Subscription.objects.filter(client=user)
    return clients_subscriptions.exists()


def check_if_valid_monthly_subscription_is_added(user):
    monthly_sub = Subscription.objects.get(
        client=user,
        billing_type='monthly'
    )
    if monthly_sub:
        monthly_sub.date_created += timedelta(weeks=4)
        monthly_sub.save()
        return True
    else:
        return False


def check_if_user_has_valid_type(user):
    if user.subscriptions.filter(
            user_type=UserTypes.INDIVIDUAL
    ).exists():
        return True
    elif user.subscriptions.filter(
            user_type=UserTypes.BUSINESS
    ).exists():
        return True
    else:
        return False


def check_if_user_has_invalid_subscription(user):
    return user.subscriptions.filter(
        is_active=False,
        date_created__lt=timezone.now()
    ).exists()


def check_if_user_has_monthly_subscription(user):
    return user.subscriptions.filter(
        is_active=True,
        billing_type=BillingType.MONTHLY
    ).exists()


def check_if_user_has_yearly_subscription(user):
    return user.subscriptions.filter(
        is_active=True,
        billing_type=BillingType.YEARLY
    ).exists()


def check_user_has_valid_billing_type(user):
    valid_type = user.subscriptions.values_list('billing_type', flat=True).get(
        billing_type__in=[BillingType.YEARLY, BillingType.MONTHLY]
    )
    if valid_type in ['monthly', 'yearly']:
        return True
    return False


def check_all_users_with_valid_sub():
    all_users = User.objects.all().filter(subscriptions__is_active=True).count()
    return all_users


def check_all_user_subscriptions(user):
    all_user_subscriptions = Subscription.objects.filter(client=user)
    return all_user_subscriptions

def check_is_active_when_outdated(user):
    pass