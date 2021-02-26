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
    """ Get and format the order lines for email display """

    ordered_items = list(order.lineitems.all())
    item_list = ''
    for item in ordered_items:
        item_list += f'x{str(item.quantity).ljust(3)}  {item.product.name} '
        item_list += f'@ £{item.product.price} ea.' + '\r\n'
        if item.product.customizable:
            item_list += ('      ' +
                          '(your customized invite will be emailed shortly)' +
                          '\r\n')
        item_list += '\r\n'

    return item_list


def check_invites_required(order):
    """ Check order items and return any invites for download links """

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
    """ Generate the customers invite design image and return url """

    filename = 'cInv' + secrets.token_urlsafe(32) + str(invite["order_number"])

    # Prepare raw image
    if settings.USING_AWS:
        image_url = invite['raw_image_url']
        print(f'Image URL: -[{image_url}]-')
    else:
        image_url = settings.DEV_BASE_URL + invite['raw_image_url']

    try:
        response = requests.get(image_url, stream=True)

    except OSError as e:
        print('Failed loading image: ', e)
        url_to_send = 'Failed to load image'

    else:
        print('Trying to process the image')
        im = Image.open(response.raw)
        print('Opened the image')
        img = im.convert("RGBA")
        image_size = img.size
        draw = ImageDraw.Draw(img)
        print('Drawn the image')

        # Apply customised fields
        if settings.USING_AWS:
            font_root = settings.MEDIA_URL + 'fonts/'
        else:
            font_root = settings.MEDIA_ROOT + '/' + 'fonts/'

        print(f'Font folder is: {font_root}')

        invite_structure = json.loads(invite['invite_data'])

        print('Loaded invite data')

        for part in invite_structure:
            pos = part['font'].index("'", 2)
            font_ttf_name = part['font'][1:pos].replace(' ', '') + '.ttf'
            font_ttf_path = font_root + font_ttf_name
            font = ImageFont.truetype(font_ttf_path, int(part['raw_size']))
            print(f'Using font: {font_ttf_path}')
            part_size = font.getsize(part['text'])
            x_pos = (image_size[0] - part_size[0]) / 2
            stroke_width = int(part['stroke_width'].replace('px', '')) * 2
            draw.text((x_pos, part['y_pos']), part['text'], part['color'],
                      font=font, stroke_width=stroke_width,
                      stroke_fill=part['stroke_fill'])

        print('finished loop of fields')

        # Save the invite as PNG and PDF
        if settings.USING_AWS:
          save_path = settings.MEDIA_URL + filename
        else:
          save_path = settings.MEDIA_ROOT + '/' + filename

        print(f'Save path: {save_path}')

        try:
            print('Trying to save PNG and PDF')
            img.save(save_path + '.png', resolution=300)
            im_pdf = img.convert('RGB')
            im_pdf.save(save_path + '.pdf', resolution=300)
        except OSError as e:
            print(f'Save error, saving: {save_path}.png | error {e}')
            url_to_send = 'save_error'

        if settings.USING_AWS:
            url_to_send = settings.MEDIA_URL + filename
            print(f'URL filename: -[{url_to_send}]-')
        else:
            url_to_send = settings.BASE_URL + settings.MEDIA_URL + filename

    return url_to_send


def send_customer_emails(request, event_type, stripe_pid, billing_details):
    """ Send an email order confirmation to the customer and
        if they have ordered any invites generate the image
        and email the download links
    """
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
        send_mail(f'-INVITATIONS- Your confirmation for order: {order.pk:010}',
                  email_body,
                  settings.DEFAULT_FROM_EMAIL,
                  [order.email])

        invites_to_send = check_invites_required(order)
        if invites_to_send:
            invite_list = ''
            for invite in invites_to_send:
                invite_list += invite['name'] + '\r\n'
                invite_url = generate_invite(invite)
                invite_list += (f'   PDF download link: {invite_url}.pdf' +
                                '\r\n' +
                                f'   PNG download link: {invite_url}.png' +
                                '\r\n\r\n')

            context = {
                'order_number': order.pk,
                'name': order.full_name,
                'order_date': order.order_date,
                'invite_link_list': invite_list,
                'sales_email': settings.DEFAULT_FROM_EMAIL,
            }
            email_body = render_to_string(
                'checkout/emails/email_invite_body.txt',
                context)
            send_mail('-INVITATIONS- Your invite download ' +
                      f'links for order: {order.pk:010}',
                      email_body,
                      settings.DEFAULT_FROM_EMAIL,
                      [order.email])

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
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the stripe events
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        payment_id = payment_intent.id
        billing_details = payment_intent.charges.data[0].billing_details
        return send_customer_emails(request, event.type,
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
