from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from orders.application.filters.order_filter import OrderFilter
from orders.domain.models import Order
from orders.application.order_serializer import OrderSerializer
from restaurants.domain.models import Restaurant
from users.application.permissions import IsDealer
from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination

@extend_schema(request=OrderSerializer, methods=["POST"])
class General(APIView):
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    
    def get(self, request):
        if not IsDealer().has_permission(request, self):
            return Response(
                {"error": "Your current user is not dealer"},
                status=status.HTTP_403_FORBIDDEN,
            )
        orders = Order.objects.filter(active=True)

        filterset = self.filterset_class(request.GET, queryset=orders)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        filtered_orders = filterset.qs

        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size')
        if page_size:
            paginator.page_size = int(page_size)
        result_page = paginator.paginate_queryset(filtered_orders, request)

        serializer = OrderSerializer(result_page, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not IsDealer().has_permission(request, self):
            return Response(
                {"error": "Your current user is not dealer"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetByRestaurant(APIView):
    def get(self, request, restaurant_pk):
        if not IsDealer().has_permission(request, self):
            return Response(
                {"error": "Your current user is not dealer"},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        try:
            restaurant = Restaurant.objects.get(id=restaurant_pk)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        orders = Order.objects.filter(active=True, restaurant=restaurant)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class EditStatus(APIView):
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, active=True)

        if not IsDealer().has_permission(request, self):
            return Response(
                {"error": "You do not have permission to update the order status."},
                status=status.HTTP_403_FORBIDDEN,
            )

        status_update = request.data.get("status")
        if not status_update:
            return Response(
                {"error": "Status is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_update
        order.save()
        return Response(
            {"message": "Order status updated successfully."}, status=status.HTTP_200_OK
        )
