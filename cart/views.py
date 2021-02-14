from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_cart(request):
    """ A view to show the shopping cart """

    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ A view to add an item to the shopping cart """

    quantity = int(request.POST.get(f'qty-item-{product_id}'))
    original_path = request.POST.get('original_path')
    if quantity < 100:
        cart = request.session.get('cart', {})
        product = get_object_or_404(Product, pk=product_id)

        if product_id in list(cart.keys()):
            cart[product_id] += quantity
            messages.success(request, f'{product.name} quantity has been \
                                      updated to {cart[product_id]}.',
                                      extra_tags='updated shopping cart')
            request.session['cart'] = cart

        else:
            cart[product_id] = quantity
            messages.success(request, f'(x{cart[product_id]}) {product.name}\
                                      {" has" if quantity == 1 else " have"} \
                                      been added to your shopping cart.',
                                      extra_tags='added to shopping cart')
            request.session['cart'] = cart

    else:
        messages.error(request, 'Please enter a quantity less than 100 or \
                                contact our sales team to discuss large \
                                orders.',
                                extra_tags='shopping cart quantity')
    return redirect(original_path)


def remove_item(request, product_id):
    """ A view to remove an item from the shopping cart
        if the product exists in the cart
    """
    try:
        product = Product.objects.get(pk=product_id)
        cart = request.session.get('cart', {})
        cart.pop(product_id)
    except (Product.DoesNotExist, KeyError):
        messages.error(request, f'Product code [{product_id}] has not been \
                                found in your cart.',
                                extra_tags='shopping cart')
    else:
        request.session['cart'] = cart
        messages.success(request, f'{product.name} \
                                  has been removed from your shopping cart.',
                                  extra_tags='removed from shopping cart')

    return render(request, 'cart/cart.html')


def update_cart_qty(request):
    """ Update all the quantities in the shopping cart
        Report error if qty > 99
        Delete from cart if the qty was set to 0
    """
    form_data = list(request.POST.items())
    cart = {}
    quantities_changed = False
    error_msg = ''

    for product_id_element, item_quantity in form_data:
        if product_id_element[0:3] == 'qty':
            item_quantity = int(item_quantity)
            if item_quantity > 0:
                if item_quantity > 99:
                    item_quantity = 1
                    error_msg = 'However, one or more product quantities were set \
                                above 99. Please enter quantities less than \
                                100 or contact our sales team to discuss \
                                large orders.'
                product_id = product_id_element.split('-')[-1]
                cart[product_id] = item_quantity
                quantities_changed = True

            if item_quantity == 0:
                quantities_changed = True

    if quantities_changed:
        request.session['cart'] = cart
        messages.success(request, f'Shopping cart quantities have been \
                                  updated. {error_msg}',
                                  extra_tags='shopping cart quantities')
    else:
        messages.success(request, 'Quantity error, please double-check your \
                                  quantities and click [Update Cart].',
                                  extra_tags='shopping cart quantities')

    return render(request, 'cart/cart.html')
