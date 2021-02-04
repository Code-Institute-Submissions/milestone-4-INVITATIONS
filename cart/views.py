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
