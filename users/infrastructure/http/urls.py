from django.urls import path
from .user_controller import UserController

urlpatterns = [
    path('', UserController.as_view(), name='user-list'),  # GET /users/
]
