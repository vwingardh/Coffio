from django.http.response import JsonResponse

from cart.cart import Cart
from .models import Order, OrderItem


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        user_id = request.user.id
        order_key = request.POST.get('order_key')
        cart_total = cart.get_total_price()

        # Check if order exists in DB
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id = user_id, 
                full_name = 'Jane Smith', 
                address1 = '1854 Skyline Drive',
                address2 = '', 
                country = 'United States',
                state = 'California',
                city = 'Los Angeles',
                email = 'Jane@email.com',
                post_code = '11359',
                total_paid = cart_total, 
                order_key = order_key
            )
            
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id = order_id,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['qty']
                )
            
            response = JsonResponse({'success': 'Order saved in DB'})

            return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
