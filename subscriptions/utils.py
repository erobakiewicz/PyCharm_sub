from datetime import timedelta

from django.utils import timezone

from subscriptions.models import Subscription


def check_if_user_has_valid_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
        sub_period__gte=timezone.now().date()
    ).exists()

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
            user_type="individual").exists():
        return True
    elif user.subscription_set.filter(
            user_type="business"
    ).exists():
        return True
    else:
        return False
