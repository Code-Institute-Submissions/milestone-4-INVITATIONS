from django.shortcuts import get_object_or_404
from django.conf import settings
from decimal import Decimal

from products.models import Product

import json


def cart_contents(request):

    cart_items = []
    cart_total = 0
    product_count = 0
    grand_total = 0

    string_cart = str(request.session.get('cart', []))
    print('Context String cart: ', string_cart)
    cart = json.loads(string_cart)

    for item in cart:
        if isinstance(item['quantity'], int):
            product = get_object_or_404(Product, pk=item['product_id'])
            line_total = item['quantity'] * product.price
            cart_total += line_total
            product_count += item['quantity']
            cart_items.append({
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'name': product.name,
                'price': product.price,
                'image': product.view_image,
                'line_total': line_total,
                'invite_data': item['invite_data'],
            })
            print('Custom is: ', item['invite_data'])

    if cart_total < settings.FREE_DELIVERY_AMOUNT:
        delivery = settings.STANDARD_DELIVERY_CHARGE
    else:
        delivery = 0

    grand_total = (delivery + cart_total)

    context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'cart_product_count': product_count,
            'cart_delivery': delivery,
            'cart_grand_total': grand_total,
        }

    return context
