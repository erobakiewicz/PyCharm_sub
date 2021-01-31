from django.utils import timezone

from orders.constants import OrderStatus


def check_if_subscription_is_ordered(user):
    return user.order.filter(
        order_status=OrderStatus.IN_PROGRESS,
    ).exists()
