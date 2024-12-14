from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from restaurants.domain.models import Restaurant


class RestaurantController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        restaurants = Restaurant.objects.all()
        data = [{"id": restaurant.id} for restaurant in restaurants]
        return Response(data)