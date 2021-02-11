from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from .models import Order
from products.models import Product

from .forms import OrderForm
from cart.contexts import cart_contents
from decimal import Decimal

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


def calculate_order_amount(order_items):
    """ Re-calculate the order total using the database price """

    # print('Shopping cart:', order_items)
    order_total = 0
    grand_total = 0

    for item in order_items:
        product = get_object_or_404(Product, pk=item['product_id'])
        database_price = product.price
        product_total = Decimal(database_price * item['quantity'])
        order_total += int(product_total * 100)

    if order_total < (settings.FREE_DELIVERY_AMOUNT * 100):
        delivery = int(settings.STANDARD_DELIVERY_CHARGE * 100)
    else:
        delivery = 0

    grand_total = order_total + delivery
    return grand_total


@csrf_exempt
def create_payment_intent(request):
    try:
        # data = json.loads(request.body)
        # print('Data:', data)
        current_shopping_cart = cart_contents(request)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(current_shopping_cart['cart_items']),
            currency='gbp',
            description='Test description',
            metadata={
                    'hello': 'World',
                    'supper': 'Cornflakes',
            },
        )
        print('Intent: ', intent['client_secret'])
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print('Error:', e)
        return JsonResponse({'error': str(e)})
