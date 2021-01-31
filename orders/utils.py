

def check_if_subscription_is_ordered(user):
    return user.subscriptions.filter().exists()

def check_if_sub_is_expensive(order, expensive):
    if order.price < expensive:
        return True
    else:
        return False

def check_if_sub_and_order_has_the_same_client(order, subscription):
    return order.subscription.client.id == subscription.client.id

