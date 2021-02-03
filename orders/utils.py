from django.utils import timezone

from orders.constants import OrderStatus
from orders.models import Order


def check_if_subscription_is_ordered(user):
    return user.subscriptions.filter().exists()


def check_if_sub_is_expensive(order, expensive):
    if order.price < expensive:
        return True
    else:
        return False


def check_if_sub_and_order_has_the_same_client(order, subscription):
    return order.subscription.client.id == subscription.client.id


class NewOrder:
    errors = {}
    new_order = None

    def __init__(self, subscription):
        self.subscription = subscription

    def create_order(self):
        # 1. check validation

        # 2. Create Order with subscription ID and input data email, price
        create_new_order_for_sub_id(self)

        # 3. Payment

        # 4. Set the status declined / paid
        set_order_status(self)

        # 5. IF status==declined return to payment

        # 6. IF status==paid send email notification ORDER COMPLETE


def create_new_order_for_sub_id(self):
    try:
        new_order = Order.objects.create(subscription_id=self.id,
                                         order_status=OrderStatus.IN_PROGRESS,
                                         created=timezone.now().date(),
                                         updated=timezone.now().date(),
                                         email="test@test.com",
                                         price=100,
                                         )
        return new_order
    except:
        raise Exception("Creation order error")


def set_order_status(new_order, status):
    if status == OrderStatus.PAID:
        new_order.order_status = OrderStatus.PAID
        return new_order.order_status
    else:
        new_order.order_status = OrderStatus.DECLINED
        return new_order.order_status
