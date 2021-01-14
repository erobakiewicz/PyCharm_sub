from django.utils import timezone


def check_if_user_has_valid_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
        sub_period__gte=timezone.now().date()
    ).exists()
