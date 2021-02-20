from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_checkout, name='view_checkout'),
    path('create-payment-intent/',
         views.create_payment_intent,
         name='create_payment_intent'),
    path('success/<order_number>',
         views.checkout_success, name='checkout_success'),
    path('history/<order_number>',
         views.order_history, name='order_history'),
    path('webhook/', views.webhook_view, name='webhook_view'),
]
