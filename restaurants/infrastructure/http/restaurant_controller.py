from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from restaurants.domain.models import Restaurant
from restaurants.application.restaurant_serializer import RestaurantSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from restaurants.application.filters.restaurant_filter import RestaurantFilter
from drf_spectacular.utils import extend_schema


@extend_schema(request=RestaurantSerializer, methods=["POST"])
class GetPost(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter

    def get(self, request):
        restaurants = Restaurant.objects.filter(active=True)
        filterset = self.filterset_class(request.GET, queryset=restaurants)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        filtered_restaurants = filterset.qs

        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size')
        if page_size:
            paginator.page_size = int(page_size)
        result_page = paginator.paginate_queryset(filtered_restaurants, request)
        serializer = RestaurantSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['active'] = True
        serializer = RestaurantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=RestaurantSerializer, methods=["PATCH"])
class EditOrDelete(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk, active=True)
        serializer = RestaurantSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        restaurant = get_object_or_404(Restaurant, pk=pk, active=True)
        restaurant.active = False
        restaurant.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
