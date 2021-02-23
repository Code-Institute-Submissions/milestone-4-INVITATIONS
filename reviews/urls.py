from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews, name='reviews'),
    path('add/<int:product_id>/<int:order_id>/', views.add_review, name='add_review'),
]
