def check_if_sub_and_order_has_the_same_client(order, subscription):
    return order.subscription.client.id == subscription.client.id
