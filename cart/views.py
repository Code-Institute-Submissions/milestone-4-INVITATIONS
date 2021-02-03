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
