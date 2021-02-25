from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from decimal import Decimal

from django.conf import settings
from .models import Order, OrderLineItem
from products.models import Product
from django.contrib.auth.models import User

from .forms import OrderForm
from cart.contexts import cart_contents
import json

import stripe
from .webhooks import webhook_view
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def view_checkout(request):
    """ A view to show the checkout form and save the order """

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
                json_item['invite_data'] = item['invite_data']
                json_cart.append(json_item)

            order.original_cart = json.dumps(json_cart)

            if request.user.is_authenticated:
                profile = User.objects.get(username=request.user)
                order.user = profile

            order.save()
            for item in original_cart:
                product = get_object_or_404(Product, pk=item['product_id'])
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=Decimal(item['quantity']),
                    invite_data=item['invite_data'],
                )
                order_line_item.save()

            messages.success(request,
                             f'Thank you, payment of £{order.grand_total:.2f} \
                             successfully received. Your order number is \
                             [{order.pk:010}]. Full order confirmation details\
                             are displayed below.',
                             extra_tags='Order confirmation')
            return redirect(reverse('checkout_success', args=[order.pk]))

        else:
            messages.error(request, 'There was an error with your form entry, \
                 please contact our sales team to check your order details, \
                 as payment may have already been processed. Thank you')
    else:
        form_data = {}
        if request.user.is_authenticated:
            form_data = {
                'full_name': f'{request.user.first_name.title()} '
                             f'{request.user.last_name.title()}',
                'email': request.user.email,
            }

        form = OrderForm(initial=form_data)
        context = {
            'form': form,
        }
        return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """ Display successful order confirmation """

    if request.user.is_authenticated:
        try:
            order = Order.objects.get(pk=order_number)
        except Order.DoesNotExist:
            messages.error(request,
                           f'Sorry cannot locate confirmation data for \
                           order number {int(order_number):010}',
                           extra_tags='order confirmation')

            return redirect('home')

        else:
            if order.user == request.user:
                context = {
                    'order': order,
                }

                if 'cart' in request.session:
                    del request.session['cart']

                return render(request, 'checkout/success.html', context)

    messages.error(request,
                   f'Sorry cannot view the confirmation for order number \
                   {int(order_number):010}',
                   extra_tags='order confirmation')

    return redirect('home')


def order_history(request, order_number):
    """ Display an historic order confirmation from user profile """

    if request.user.is_authenticated:
        try:
            order = Order.objects.get(pk=order_number)
        except Order.DoesNotExist:
            messages.error(request,
                           'Sorry that order confirmation cannot be found',
                           extra_tags='order confirmation')

            return redirect('user_profile')

        else:
            if order.user == request.user:
                context = {
                    'order': order,
                    'order_history': True,
                }

                return render(request, 'checkout/success.html', context)

    messages.error(request,
                   'Sorry cannot access that order history.',
                   extra_tags='order history')

    return redirect('home')


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
    """ Create stripe payment intent and pass back to client """

    current_shopping_cart = cart_contents(request)
    ordered_by = request.user
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(current_shopping_cart['cart_grand_total'] * 100),
            currency='gbp',
            metadata=shopping_cart_items(ordered_by,
                                         current_shopping_cart['cart_items']),
        )
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        messages.error(request, 'Problem contacting the Stripe payment  \
                                system, please retry your payment later.',
                                extra_tags='payment processing')
        return JsonResponse({'error': str(e)}, status=400)
