from django.shortcuts import render


def view_cart(request):
    """ A view to show the shopping cart """

    return render(request, 'cart/cart.html')
