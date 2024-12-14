from django.urls import path
from .order_controller import OrderController

urlpatterns = [
    path('', OrderController.as_view(), name='order-list'),
]
