from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from subscriptions.models import Subscription

from subscriptions.constants import BillingType, UserTypes, SpecialOffers




def check_if_user_has_valid_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
        sub_period__gte=timezone.now().date()
    ).exists()


def check_if_subscription_was_added_to_user(user):
    sub = Subscription.objects.create(
        client=user,
        sub_period=timezone.now(),
        is_active=True,
        user_type=UserTypes.INDIVIDUAL,
        billing_type=BillingType.MONTHLY,
        special_offers=SpecialOffers.NO_SPECIAL_OFFERS,
        us_tax=False,
        price=1000,
    )
    if sub:
        return True
    return False



def check_if_valid_monthly_subscription_is_added(user):
    monthly_sub = Subscription.objects.get(
        client=user,
        billing_type='monthly'
    )
    if monthly_sub:
        monthly_sub.sub_period += timedelta(weeks=4)
        monthly_sub.save()
        return True
    else:
        return False


def check_if_user_has_valid_type(user):
    if user.subscription_set.filter(
            user_type=UserTypes.INDIVIDUAL).exists():
        return True
    elif user.subscription_set.filter(
            user_type=UserTypes.BUSINESS
    ).exists():
        return True
    else:
        return False


def check_if_user_has_invalid_subscription(user):
    return user.subscription_set.filter(
        is_active=False,
        sub_period__lt=timezone.now()
    ).exists()


def check_if_user_has_monthly_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
        billing_type=BillingType.MONTHLY
    ).exists()


def check_if_user_has_yearly_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
        billing_type=BillingType.YEARLY
    ).exists()


def check_all_users_with_vaild_sub():
    all_users = User.objects.all().filter(subscription__is_active=True).count()
    return all_users