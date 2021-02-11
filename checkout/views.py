from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Order
from .forms import OrderForm
from django.conf import settings

import stripe
import json
from django.http import JsonResponse
import os

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_checkout(request):
    """ A view to show the checkout form and order summary """

    form = OrderForm()

    context = {
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@csrf_exempt
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        print('Data:', data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='gbp'
        )
        print('Intent: ', intent['client_secret'])
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print('Error:', e)
        return JsonResponse({'error': str(e)})
