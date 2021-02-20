from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail

from .models import Order

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def get_order_details(request, stripe_pid):
    """ Get the matching order details """
    try:
        order = Order.objects.get(stripe_pid=stripe_pid)
    except Order.DoesNotExist:
        order = False

    return order


def format_shipping_address(order):
    """ Format the shipping address so it displays neatly """
    shipping_address = f'{order.street_address1.title()}' + '\r\n'
    if order.street_address2:
        shipping_address += f'{order.street_address2.title()}' + '\r\n'
    shipping_address += f'{order.town_or_city.title()}' + '\r\n'
    if order.postcode:
        shipping_address += f'{order.postcode.upper()}' + '\r\n'
    shipping_address += f'{order.country}'
    return shipping_address


def format_order_items(order):
    """ Get and format the order lines for display """
    ordered_items = list(order.lineitems.all())
    item_list = ''
    for item in ordered_items:
        item_list += f'x{str(item.quantity).ljust(3)}  {item.product.name} '
        item_list += f'@ £{item.product.price} ea.' + '\r\n'
        if item.product.customizable:
            item_list += '      '
            item_list += '(your customized invite will be emailed shortly)'
            item_list += '\r\n'
        item_list += '\r\n'

    return item_list


def check_invites_required(order):
    """ Check if any invite downloads required """
    ordered_items = list(order.lineitems.all())
    invites = []
    for item in ordered_items:
        if item.product.customizable:
            invite = {
               'product_id': item.product.pk,
               'name': item.product.name,
               'invite_data': item.invite_data,
            }
            invites.append(invite)
    return invites


def send_email_confirmation(request, event_type, stripe_pid, billing_details):
    """ Send an email confirmation to the customer """
    order = get_order_details(request, stripe_pid)
    if order:
        context = {
            'order': order,
            'shipping_address': format_shipping_address(order),
            'ordered_items': format_order_items(order),
            'sales_email': settings.DEFAULT_FROM_EMAIL,
        }
        email_body = render_to_string(
            'checkout/emails/email_confirmation_body.txt',
            context)
        send_mail(f'-INVITATIONS- confirmation for order: {order.pk:010}',
                  email_body,
                  settings.DEFAULT_FROM_EMAIL,
                  [order.email])

        invites_to_send = check_invites_required(order)
        print(f'Invites to send: {invites_to_send}')

        response_content = f'Webhook OK:{event_type}, customer emailed'

    else:
        response_content = f'Webhook OK:{event_type}, order NOT found'

    return HttpResponse(
        content=response_content,
        status=200)


@require_POST
@csrf_exempt
def webhook_view(request):
    """ Function to listen and process the Stripe webhooks """
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
        return HttpResponse(
            content=f'Webhook OK:{event.type}, pay intent FAILED',
            status=200)

    else:
        return HttpResponse(
            content=f'Webhook OK:{event.type}, NOT handled',
            status=200)
