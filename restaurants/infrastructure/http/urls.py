from django.urls import path
from .restaurant_controller import RestaurantController

urlpatterns = [
    path('', RestaurantController.as_view(), name='restaurant-list'),
]
