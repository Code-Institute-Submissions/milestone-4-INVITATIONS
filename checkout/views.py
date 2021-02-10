from django.shortcuts import render

from .models import Order
from .forms import OrderForm


def view_checkout(request):
    """ A view to show the checkout form and order summary """

    order_form = OrderForm()

    context = {
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)
