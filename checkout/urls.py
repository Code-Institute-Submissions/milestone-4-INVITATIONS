from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_checkout, name='view_checkout'),
    path('create-payment-intent/',
         views.create_payment_intent,
         name='create_payment_intent'),
]
