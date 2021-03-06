from django.shortcuts import render, redirect
from django.contrib import messages

from products.models import Product

import json


def view_cart(request):
    """ A view to show the shopping cart """

    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ A view to add an item to the shopping cart
        if there are no qty / product errors
    """

    if request.POST.get(f'qty-item-{product_id}') is not None:
        quantity = int(request.POST.get(f'qty-item-{product_id}'))
        original_path = request.POST.get('original_path')
        if quantity < 100:
            string_cart = str(request.session.get('cart', []))
            cart = json.loads(string_cart)
            try:
                product = Product.objects.get(pk=product_id)
            except (Product.DoesNotExist):
                messages.error(request,
                               f'Product code [{product_id}] has not been \
                               found. Please retry.',
                               extra_tags='shopping cart')
            else:
                invite_data = request.POST.get(f'invite-data-{product_id}')
                item_already_in_cart = False
                for item in cart:
                    if item['product_id'] == product_id:
                        if product.customizable:
                            item['quantity'] = 1
                            messages.success(request,
                                             f'{product.name} is already in \
                                             your shopping cart. Please note \
                                             invites have a fixed quantity of \
                                             1, as you can print them yourself\
                                              as many times as required.',
                                             extra_tags='shopping cart')
                            return redirect(original_path)

                        else:
                            item['quantity'] += quantity
                            if item['quantity'] > 99:
                                item['quantity'] = 99
                                message = f'{product.name} quantity has been \
                                           set to {item["quantity"]} as you \
                                           cannot order more than 99 of \
                                           one item.  If you need to order \
                                           more please contact our sales team.'
                            else:
                                message = f'{product.name} quantity has been \
                                           updated to {item["quantity"]}.'
                            messages.success(request, message,
                                             extra_tags='shopping cart')
                            item_already_in_cart = True

                if not item_already_in_cart:
                    new_item = {
                        'product_id': product_id,
                        'quantity': quantity,
                        'invite_data': invite_data,
                    }
                    cart.append(new_item)
                    messages.success(request,
                                     f'(x{quantity}) {product.name}\
                                     {" has" if quantity == 1 else " have"} \
                                     been added to your shopping cart.',
                                     extra_tags='added to shopping cart')

                request.session['cart'] = json.dumps(cart)

        else:
            messages.error(request,
                           'Please enter a quantity less than 100 or contact\
                           our sales team to discuss large orders.',
                           extra_tags='shopping cart quantity')

        return redirect(original_path)

    messages.error(request,
                   'Invalid product or quantity entered, please retry.',
                   extra_tags='shopping cart quantity')

    return render(request, 'cart/cart.html')


def remove_item(request, product_id):
    """ A view to remove an item from the shopping cart
        if the product exists in the cart and the database
    """
    try:
        int(product_id)
        product = Product.objects.get(pk=product_id)
        string_cart = str(request.session.get('cart', []))
        cart = json.loads(string_cart)
        for i, item in enumerate(cart):
            if item['product_id'] == product_id:
                del cart[i]
    except (Product.DoesNotExist, ValueError, KeyError):
        messages.error(request,
                       f'Product code [{product_id}] has not been \
                       found in your cart.',
                       extra_tags='shopping cart')
    else:
        request.session['cart'] = json.dumps(cart)
        messages.success(request,
                         f'{product.name} \
                         has been removed from your shopping cart.',
                         extra_tags='removed from shopping cart')

    return render(request, 'cart/cart.html')


def update_cart_qty(request):
    """ Update all the quantities in the shopping cart
        Report error if qty > 99
        Delete from cart if the qty was set to 0
    """
    form_data = list(request.POST.items())
    form_data.pop(0)
    cart = []
    quantities_changed = False
    error_msg = ''

    data_it = iter(form_data)
    if (len(form_data) % 2 == 0):
        for item, value in data_it:
            product_id = item.split('-')[-1]
            try:
                product = Product.objects.get(pk=int(product_id))
            except (Product.DoesNotExist):
                messages.error(request,
                               f'Product code [{product_id}] has not been \
                               found. Please retry.',
                               extra_tags='shopping cart')
                return render(request, 'cart/cart.html')

            else:
                if product.customizable:
                    item_quantity = 1
                else:
                    item_quantity = int(value)

                invite_data_field = next(data_it)
                invite_data = invite_data_field[1]

                if item_quantity > 0:
                    if item_quantity > 99:
                        item_quantity = 1
                        error_msg = 'However, one or more product quantities \
                                    were above 99. Please enter quantities \
                                    less than 100 or contact our sales team \
                                    to discuss large orders.'

                    new_item = {
                            'product_id': product_id,
                            'quantity': item_quantity,
                            'invite_data': invite_data,
                        }
                    cart.append(new_item)

                    quantities_changed = True

                if item_quantity == 0:
                    quantities_changed = True

    if quantities_changed:
        request.session['cart'] = json.dumps(cart)
        messages.success(request,
                         f'Your shopping cart has been \
                         updated. {error_msg}',
                         extra_tags='shopping cart')
    else:
        messages.error(request,
                       'Quantity error, please double-check your \
                       quantities and click [Update Cart].',
                       extra_tags='shopping cart')

    return render(request, 'cart/cart.html')
