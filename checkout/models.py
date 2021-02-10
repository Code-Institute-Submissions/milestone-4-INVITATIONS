from django.db import models
from django.conf import settings
from django.db.models import Sum

from django_countries.fields import CountryField

from products.models import Product


class Order(models.Model):
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
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
        """
        When an item line is added calculate the grand total
        """
        result = self.lineitems.aggregate(total=Sum('lineitem_total'))
        self.order_total = result['total']

        print('Order total:', self.order_total)
        print(type(self.order_total))

        print('Delivery check:', settings.FREE_DELIVERY_AMOUNT)
        print(type(settings.FREE_DELIVERY_AMOUNT))

        if self.order_total is not None:
            if self.order_total > settings.FREE_DELIVERY_AMOUNT:
                self.delivery_cost = 0
            else:
                self.delivery_cost = settings.STANDARD_DELIVERY_CHARGE

            self.grand_total = self.order_total + self.delivery_cost
            self.save()

    def __str__(self):
        return str(self.pk)


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False,
                              blank=False, on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=False,
                                blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override save method to calculate the lineitem total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} on order {self.order.pk}'