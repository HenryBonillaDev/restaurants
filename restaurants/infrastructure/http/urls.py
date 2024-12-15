from django.urls import path
from .restaurant_controller import EditOrDelete, GetPost

urlpatterns = [
    path('', GetPost.as_view(), name='restaurant-get-post'),
    path('<uuid:pk>',EditOrDelete.as_view(), name='restaurant-delete-patch')
]
