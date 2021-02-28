from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('our_story/', views.our_story, name='our_story'),
    path('terms_conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('delivery_info/', views.delivery_info, name='delivery_info'),
    path('contact_us/', views.contact_us, name='contact_us'),
]
