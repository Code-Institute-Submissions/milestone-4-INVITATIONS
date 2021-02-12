from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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

    if request.POST:
        current_shopping_cart = cart_contents(request)
        grand_total = current_shopping_cart['cart_grand_total']
        print('Rec-POST, save order & order-lines')
        messages.success(request, 'Thank you, payment received for '
                                  f'£{grand_total}.\r\n'
                                  'Your order confirmation is below.',
                                  extra_tags='Order confirmation')
        print('empty the shopping cart')
        return render(request, 'checkout/success.html')

    form = OrderForm()
    context = {
        'form': form,
    }

    return render(request, 'checkout/checkout.html', context)


def shopping_cart_items(ordered_by, items):
    """ Create metadata containing the order line items to pass to stripe """
    meta_data = {}
    meta_data['ordered-by-user'] = ordered_by
    for (i, item) in enumerate(items):
        meta_key = f'line-{i+1} for product-id-{item["product_id"]} '
        meta_value = f'x{item["quantity"]} of the "'
        meta_value += f'{item["name"][0:40]}..."  @  £{item["price"]} ea. | '
        meta_value += f'Product Total: £{item["line_total"]}'
        meta_data[meta_key] = meta_value

    return meta_data


@csrf_exempt
def create_payment_intent(request):
    current_shopping_cart = cart_contents(request)
    ordered_by = request.user
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(current_shopping_cart['cart_grand_total'] * 100),
            currency='gbp',
            metadata=shopping_cart_items(ordered_by,
                                         current_shopping_cart['cart_items']),
        )
        print('Intent: ', intent['client_secret'])
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        print('Error:', e)
        return JsonResponse({'error': str(e)})
