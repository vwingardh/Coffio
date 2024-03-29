from django_countries import countries
import stripe
import json
import os

from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from order.views import payment_confirmation


@login_required 
def payment(request):
    cart = Cart(request)
    total = str(cart.get_subtotal_price())
    total = total.replace('.', '')
    total = int(total)
    # Payment intent to track entire process - sales funnel
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='usd',
        metadata={'userid': request.user.id}
    )
    # Pass client intent to client side - embed in template
    # Embed in data attribute to be extracted with JS to complete payment
    return render(request, 'payment/payment.html', {'client_secret': intent.client_secret, 'countries': countries})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))
    return HttpResponse(status=200)


@login_required 
def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'payment/orderplaced.html')
