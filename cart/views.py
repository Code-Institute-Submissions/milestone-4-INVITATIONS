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
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(request, f'{product.name} quantity has been \
                                  updated to {cart[product_id]}.',
                                  extra_tags='shopping cart updated')
    else:
        cart[product_id] = quantity
        messages.success(request, f'(x{cart[product_id]}) {product.name} \
                                  has been added to your shopping cart.',
                                  extra_tags='added to shopping cart')

    request.session['cart'] = cart
    return redirect(original_path)


def remove_item(request, product_id):
    """ A view to remove an item from the shopping cart """
    cart = request.session.get('cart', {})
    cart.pop(product_id)
    request.session['cart'] = cart
    return render(request, 'cart/cart.html')


def update_cart_qty(request):
    form_data = list(request.POST.items())
    cart = {}

    for product_id_element, item_quantity in form_data:
        if product_id_element[0:3] == 'qty':
            item_quantity = int(item_quantity)
            if item_quantity > 0:
                product_id = product_id_element.split('-')[-1]
                cart[product_id] = item_quantity

    request.session['cart'] = cart
    return render(request, 'cart/cart.html')
