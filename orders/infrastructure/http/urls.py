from django.urls import path
from .order_controller import EditStatus, General, GetByRestaurant

urlpatterns = [
    path('', General.as_view(), name='orders'),
    path('<uuid:pk>/change-status',EditStatus.as_view(), name='edit-orders'),
    path('restaurant/<uuid:restaurant_pk>', GetByRestaurant.as_view(), name='get-orders-by-restaurant')
]
