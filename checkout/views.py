from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from .models import Order
from products.models import Product

from .forms import OrderForm
from cart.contexts import cart_contents

import stripe
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_checkout(request):
    """ A view to show the checkout form and order summary """

    form = OrderForm()

    context = {
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context)


def shopping_cart_items(items):
    """ Create metadata containing the order line items to pass to stripe """
    meta_data = {}
    for (i, item) in enumerate(items):
        meta_key = f'Line-{i+1} for product-id({item["product_id"]})'
        meta_value = f'{item["name"][0:40]}... | '
        meta_value += f'x({item["quantity"]}) @ £{item["price"]} ea. | '
        meta_value += f'Product Total: £{item["line_total"]}'
        meta_data[meta_key] = meta_value

    return meta_data


@csrf_exempt
def create_payment_intent(request):
    current_shopping_cart = cart_contents(request)
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(current_shopping_cart['cart_grand_total'] * 100),
            currency='gbp',
            metadata=shopping_cart_items(current_shopping_cart['cart_items']),
        )
        print('Intent: ', intent['client_secret'])
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print('Error:', e)
        return JsonResponse({'error': str(e)})
