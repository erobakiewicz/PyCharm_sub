from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'is_active', 'user_type', 'billing_type',
                    'special_offers')
    list_filter = ('client', 'is_active')
