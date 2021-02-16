from rest_framework import serializers

from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'client',
            'is_active',
            'user_type',
            'billing_type',
            'special_offers',
            'date_created',
            'valid_till',
            'valid_from',
        ]


