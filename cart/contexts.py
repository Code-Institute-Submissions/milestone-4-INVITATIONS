def cart_contents(request):

    cart_items = []
    cart_total = 0
    product_count = 5
    delivery = 6
    grand_total = 0

    cart = request.session.get('cart', {})

    context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'cart_product_count': product_count,
            'cart_delivery': delivery,
            'cart_grand_total': grand_total,
        }

    return context
