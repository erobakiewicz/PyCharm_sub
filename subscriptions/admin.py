from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'sub_period','is_active','user_type','billing_type',
                    'special_offers','sub_quantity','us_tax','price')
    list_filter = ('client', 'sub_period','is_active')
