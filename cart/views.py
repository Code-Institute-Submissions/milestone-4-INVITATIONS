from django.shortcuts import render, redirect


def view_cart(request):
    """ A view to show the shopping cart """

    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ A view to add an item to the shopping cart """

    quantity = 1
    original_path = request.POST.get('original_path')
    print(f'Path: {original_path}')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        prod_there = cart[product_id] + quantity
        print(f'There count: {prod_there}')
    else:
        cart[product_id] = quantity
        print(f'New Prod count: {quantity}')
        print(f'Keys: {list(cart.keys())}')

    print(f'Cart: {cart}')
    request.session['cart'] = cart
    return redirect(original_path)


def remove_item(request, product_id):
    """ A view to remove an item from the shopping cart """
    cart = request.session.get('cart', {})

    print(cart)
    print(type(cart))
    cart.pop(product_id)
    print(cart)

    request.session['cart'] = cart
    return render(request, 'cart/cart.html')


def update_cart_qty(request):
    # form_data = request.POST.items()
    form_data = list(request.POST.items())
    print(f'Form data: {form_data}')
    print(type(form_data))
    cart = {}

    for product_id_element, item_quantity in form_data:
        print(f'Part= {product_id_element[0:3]}')
        if product_id_element[0:3] == 'qty':
            product_id = product_id_element.split('-')[-1]
            item_quantity = int(item_quantity)
            print(f'Product ID: {product_id_element} is ID: {product_id} with qty of: {item_quantity}')
            cart[product_id] = item_quantity

    request.session['cart'] = cart
    return render(request, 'cart/cart.html')
