from django.shortcuts import get_object_or_404
from django.conf import settings
from decimal import Decimal

from products.models import Product


def cart_contents(request):

    cart_items = []
    cart_total = 0
    product_count = 0
    grand_total = 0

    cart = request.session.get('cart', {})

    for product_id, item_quantity in cart.items():
        if isinstance(item_quantity, int):
            product = get_object_or_404(Product, pk=product_id)
            line_total = item_quantity * product.price
            cart_total += line_total
            product_count += item_quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': item_quantity,
                'name': product.name,
                'price': product.price,
                'image': product.view_image,
                'line_total': line_total,
            })

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
