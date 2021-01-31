from django.utils import timezone

from orders.constants import OrderStatus


def check_if_subscription_is_ordered(user):
    return user.subscriptions.filter().exists()

def check_if_sub_is_expensive(order, expensive):
    if order.price < expensive:
        return True
    else:
        return False
