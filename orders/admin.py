from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('subscription',
                  'order_status',
                  'created',
                  'updated',
                  'email',
                  'price',
        )
    list_filter = ('subscription', 'order_status')
