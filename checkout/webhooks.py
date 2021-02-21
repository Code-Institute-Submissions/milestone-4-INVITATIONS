from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from PIL import Image, ImageFont, ImageDraw

import secrets
import requests
import json

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
               'raw_image_url': item.product.raw_image.url,
               'order_number': order.pk,
               'user_id': order.user.pk,
            }
            invites.append(invite)
    return invites


def generate_invite(invite):
    """ Generate the invite design image files """
    filename = 'cInv' + secrets.token_urlsafe(32) + str(invite["order_number"])

    # Prepare raw image
    image_url = settings.BASE_URL + invite['raw_image_url']
    response = requests.get(image_url, stream=True)
    im = Image.open(response.raw)
    img = im.convert("RGBA")
    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)

    # Apply customised fields
    font_root = settings.MEDIA_ROOT + '/' + 'fonts/'
    invite_structure = json.loads(invite['invite_data'])
    for part in invite_structure:
        pos = part['font'].index("'", 2)
        font_ttf_name = part['font'][1:pos].replace(' ', '') + '.ttf'
        font_ttf_path = font_root + font_ttf_name
        font = ImageFont.truetype(font_ttf_path, int(part['raw_size']))
        part_width, part_height = font.getsize(part['text'])
        x_pos = (image_width - part_width) / 2
        stroke_width = int(part['stroke_width'].replace('px', ''))
        draw.text((x_pos, part['y_pos']), part['text'], part['color'],
                  font=font, stroke_width=stroke_width,
                  stroke_fill=part['stroke_fill'])

    # Save the invite as PNG and PDF
    save_path = settings.MEDIA_ROOT + '/' + filename
    img.save(save_path + '.png', resolution=300)
    im_pdf = img.convert('RGB')
    im_pdf.save(save_path + '.pdf', resolution=300)

    url_to_send = settings.BASE_URL + settings.MEDIA_URL + filename
    return url_to_send


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
        if invites_to_send:
            invite_items = ''
            for invite in invites_to_send:
                invite_items += invite['name'] + '\r\n'
                url_to_send = generate_invite(invite)
                invite_items += f'   PDF download link: {url_to_send}.pdf' + '\r\n'
                invite_items += f'   PNG download link: {url_to_send}.png' + '\r\n'
                invite_items += '\r\n'

            print(f'Invite items: {invite_items}')

        else:
            print('No invites to send.')

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
