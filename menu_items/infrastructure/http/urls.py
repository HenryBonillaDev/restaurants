from django.urls import path
from .menu_item_controller import MenuItemController

urlpatterns = [
    path('', MenuItemController.as_view(), name='item-list'),
]