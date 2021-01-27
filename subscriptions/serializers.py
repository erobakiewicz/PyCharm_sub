from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import serializers

from subscriptions.constants import BillingType
from subscriptions.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['client','is_active','user_type',
                  'billing_type','special_offers','date_created','valid_till']


