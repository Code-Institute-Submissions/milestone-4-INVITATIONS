from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart_items = []
    cart_total = 0
    product_count = 0
    delivery = 0
    grand_total = 0

    cart = request.session.get('cart', {})

    for product_id, item_quantity in cart.items():
        if isinstance(item_quantity, int):
            product = get_object_or_404(Product, pk=product_id)
            cart_total += item_quantity * product.price
            product_count += item_quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': item_quantity,
                'name': product.name,
                'image': product.view_image,
            })

    grand_total = delivery + cart_total

    context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'cart_product_count': product_count,
            'cart_delivery': delivery,
            'cart_grand_total': grand_total,
        }

    return context
