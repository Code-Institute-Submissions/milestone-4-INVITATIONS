from django.shortcuts import render


def view_checkout(request):
    """ A view to show the checkout form and order summary """

    return render(request, 'checkout/checkout.html')
