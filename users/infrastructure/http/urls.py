from django.urls import path
from .user_controller import Logout, UserController
from .user_controller import Register, Login, ChangePassword
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('change-password', ChangePassword.as_view(), name='change-password'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('', UserController.as_view(), name='user-list'),
]
