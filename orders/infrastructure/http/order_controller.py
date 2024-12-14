from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.domain.models import Order


class OrderController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        orders = Order.objects.all()
        data = [{"id": order.id} for order in orders]
        return Response(data)