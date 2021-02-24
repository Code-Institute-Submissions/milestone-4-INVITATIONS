from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/<int:order_id>/',
         views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
]
