from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


def send_email_confirmation(request, event_type, stripe_pid, billing_details):
    print(f'Send email of order: {stripe_pid} to {billing_details}')
    send_mail(f'Thank you for your order {stripe_pid}',
              'Message body here',
              settings.DEFAULT_FROM_EMAIL,
              ['test@test.com'])

    return HttpResponse(content=f'Webhook OK:{event_type}, customer emailed',
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
        payment_intent = event.data.object  # contains a stripe.PaymentMethod
        # handle_payment_intent_failed(payment_intent)
        print('Payment failed:---', payment_intent)
        return HttpResponse(status=200)
    # ... handle other event types
    else:
        print(f'Unhandled event type {event.type}')
        return HttpResponse(status=200)

    # return HttpResponse(status=200)
