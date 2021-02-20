from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


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
        payment_intent = event.data.object  # contains a stripe.PaymentIntent
        # handle_payment_intent_succeeded(payment_intent)
        print('PaymentIntent was successful!:---', payment_intent)
    elif event.type == 'payment_intent.payment_failed':
        payment_intent = event.data.object  # contains a stripe.PaymentMethod
        # handle_payment_intent_failed(payment_intent)
        print('Payment failed:---', payment_intent)
    # ... handle other event types
    else:
        print(f'Unhandled event type {event.type}')

    return HttpResponse(status=200)
