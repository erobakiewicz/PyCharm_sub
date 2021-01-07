from django.shortcuts import render
from rest_framework import viewsets

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()