from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('webhook/', views.stripe_webhook),
]
