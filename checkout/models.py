from django.db import models
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from django.contrib.auth.models import User


class Order(models.Model):
    """ Model for order details """

    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name='order_history')
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    delivery_cost = models.DecimalField(max_digits=4, decimal_places=2,
                                        null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False,
                                  blank=False, default='')

    def update_grand_total(self):
        """ When an item line is added calculate the grand total """

        order_lines = self.lineitems.all()

        self.order_total = 0
        invites_in_cart = 0

        for item in order_lines:
            self.order_total += item.lineitem_total
            if item.product.customizable:
                invites_in_cart += 1

        if self.order_total is not None:
            if self.order_total < settings.FREE_DELIVERY_AMOUNT:
                if invites_in_cart == len(order_lines):
                    self.delivery_cost = 0
                else:
                    self.delivery_cost = settings.STANDARD_DELIVERY_CHARGE
            else:
                self.delivery_cost = 0

            self.grand_total = self.order_total + self.delivery_cost
            self.save()

    def __str__(self):
        return str(self.pk)


class OrderLineItem(models.Model):
    """ Model for order line details """

    order = models.ForeignKey(Order, null=False,
                              blank=False, on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False,
                                blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)
    invite_data = models.TextField(blank=True, default='')

    def save(self, *args, **kwargs):
        """ Override save method to calculate the lineitem total """

        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.pk}'
