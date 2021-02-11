from django.shortcuts import render

from .models import Order
from .forms import OrderForm


def view_checkout(request):
    """ A view to show the checkout form and order summary """

    form = OrderForm()

    context = {
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context)
