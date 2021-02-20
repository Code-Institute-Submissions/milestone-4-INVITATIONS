from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from .models import Order, OrderLineItem

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def get_order_details(request, stripe_pid):
    try:
        order = Order.objects.get(stripe_pid=stripe_pid)
    except Order.DoesNotExist:
        order = False

    return order


def format_shipping_address(order):
    shipping_address = f'{order.street_address1.title()}' + '\r\n'
    if order.street_address2:
        shipping_address += f'{order.street_address2.title()}' + '\r\n'
    shipping_address += f'{order.town_or_city.title()}' + '\r\n'
    if order.postcode:
        shipping_address += f'{order.postcode.upper()}' + '\r\n'
    shipping_address += f'{order.country}'

    return shipping_address


def format_order_items(order):
    print(f'Order items: {list(order.lineitems.all())}')
    ordered_items = list(order.lineitems.all())
    item_list = ''
    for item in ordered_items:
        item_list += f'x{str(item.quantity).ljust(3)}  {item.product.name} '
        item_list += f'@ £{item.product.price} ea.' + '\r\n'
        if item.product.customizable:
            item_list += '      '
            item_list += '(your customized invite will be emailed shortly)'
            item_list += '\r\n'

    return item_list


def send_email_confirmation(request, event_type, stripe_pid, billing_details):
    order = get_order_details(request, stripe_pid)
    order_data = {
        'order_number': f'{order.pk:010}',
        'order_date': f'{order.order_date}'
    }
    context = {
        'order': order,
        'shipping_address': format_shipping_address(order),
        'ordered_items': format_order_items(order),
        'sales_email': settings.DEFAULT_FROM_EMAIL,
    }
    email_body = render_to_string(
        'checkout/emails/email_confirmation_body.txt',
        context)
    if order:
        send_mail(f'-INVITATIONS- confirmation for order: {order.pk:010}',
                  email_body,
                  settings.DEFAULT_FROM_EMAIL,
                  [order.email])

        return HttpResponse(
            content=f'Webhook OK:{event_type}, customer emailed',
            status=200)
    else:
        return HttpResponse(
            content=f'Webhook OK:{event_type}, order NOT found',
            status=200)


@require_POST
@csrf_exempt
def webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the stripe event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        payment_id = payment_intent.id
        billing_details = payment_intent.charges.data[0].billing_details
        return send_email_confirmation(request, event.type,
                                       payment_id, billing_details)
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object
        print('Payment failed:---', payment_intent)
        return HttpResponse(status=200)
    else:
        print(f'Unhandled event type {event.type}')
        return HttpResponse(status=200)
