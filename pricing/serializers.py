from rest_framework import serializers

from .models import Pricing


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = [
            'offer_type',
            'user_type',
            'price_monthly',
            'price_yearly',
            'get_tax_for_monthly',
            'get_tax_for_yearly',
            'get_total_price_monthly',
            'get_total_price_yearly',
            'second_year_yearly_price',
            'third_year_onwards_yearly_price',
        ]
