from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from menu_items.domain.models import MenuItem


class MenuItemController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        items = MenuItem.objects.all()
        data = [{"id": item.id, "name": item.name, "price": item.price} for item in items]
        return Response(data)