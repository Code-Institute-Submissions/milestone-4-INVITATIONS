from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from decimal import Decimal

from django.conf import settings
from .models import Order, OrderLineItem
from products.models import Product

from .forms import OrderForm
from cart.contexts import cart_contents
import json

import stripe
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_checkout(request):
    """ A view to show the checkout form and order summary """

    if request.POST:
        current_shopping_cart = cart_contents(request)
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'stripe_pid': request.POST['stripe_pid'],
        }

        form = OrderForm(form_data)

        if form.is_valid():
            order = form.save(commit=False)
            original_cart = current_shopping_cart['cart_items']
            json_cart = []
            for item in original_cart:
                json_item = {}
                json_item['product_id'] = item['product_id']
                json_item['quantity'] = item['quantity']
                json_item['name'] = item['name']
                json_item['price'] = str(item['price'])
                json_cart.append(json_item)

            order.original_cart = json.dumps(json_cart)
            order.save()
            for item in original_cart:
                product = get_object_or_404(Product, pk=item['product_id'])
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=Decimal(item['quantity']),
                )
                order_line_item.save()

            return redirect(reverse('checkout_success', args=[order.pk]))

        else:
            messages.error(request, 'Error with form, but I reckon \
                 we have already took payment. Please check your details.')
    else:
        form = OrderForm()
        context = {
            'form': form,
        }
        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """ Process successful checkout """
    order = get_object_or_404(Order, pk=order_number)
    messages.success(request, f'Thank you, payment of £{order.grand_total} \
                              successfully received. Your order \
                              number is [{order.pk:010}] \
                              Full order confirmation is below.',
                              extra_tags='Order confirmation')

    print('Order-cart:', order.original_cart)
    print('Order-lines', order.lineitems.all)
    context = {
        'order': order,
    }

    if 'cart' in request.session:
        del request.session['cart']

    return render(request, 'checkout/success.html', context)


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
        messages.error(request, 'Problem contacting the Stripe payment  \
                                system,  please retry your payment later.',
                                extra_tags='payment processing')
        return JsonResponse({'error': str(e)}, status=400)
