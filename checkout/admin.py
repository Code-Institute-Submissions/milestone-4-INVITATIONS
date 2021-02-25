from django.contrib import admin

from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """ Admin layout details for order line items """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """ Admin layout details for orders """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_date',
                       'order_total', 'delivery_cost',
                       'grand_total', 'original_cart',
                       'stripe_pid')

    fields = ('order_date', 'full_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'postcode', 'town_or_city',
              'county', 'country', 'order_total',
              'delivery_cost', 'grand_total', 'original_cart',
              'stripe_pid')

    list_display = ('pk', 'order_date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-order_date',)


admin.site.register(Order, OrderAdmin)
