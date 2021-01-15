from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import serializers

from subscriptions.constants import BillingType
from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def create(self, validated_data):
        billing_delta = relativedelta(months=1) if validated_data['billing_type'] == BillingType.MONTHLY else relativedelta(years=1)
        validated_data['sub_period'] = timezone.now() + billing_delta
        return super().create(validated_data)
