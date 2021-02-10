from django.contrib import admin

from pricing.models import Pricing


@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('offer_type', 'user_type', 'price_monthly', 'country')
