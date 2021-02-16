from django.shortcuts import render
from rest_framework import viewsets

from pricing.models import Pricing
from pricing.serializers import PricingSerializer


class PricingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PricingSerializer
    queryset = Pricing.objects.all()
