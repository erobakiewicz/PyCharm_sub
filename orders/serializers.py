from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('subscription',
                  'order_status',
                  'created',
                  'updated',
                  'email',
                  'price',
        )