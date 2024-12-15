from django.urls import path
from .menu_item_controller import GetPost, EditOrDelete

urlpatterns = [
    path('', GetPost.as_view(), name='items-get-post'),
    path('<uuid:pk>',EditOrDelete.as_view(), name='items-delete-patch')
]