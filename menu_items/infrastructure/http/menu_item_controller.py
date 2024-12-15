from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from menu_items.domain.models import MenuItem
from menu_items.application.menu_item_serializer import MenuItemSerializer
from menu_items.application.filters.menu_item_filter import MenuItemFilter

class GetPost(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MenuItemFilter

    def get(self, request):
        menu_items = MenuItem.objects.filter(active=True)
        filterset = self.filterset_class(request.GET, queryset=menu_items)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)
        filtered_menu_items = filterset.qs
        
        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size')
        if page_size:
            paginator.page_size = int(page_size)
        result_page = paginator.paginate_queryset(filtered_menu_items, request)
        serializer = MenuItemSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=MenuItemSerializer, responses={201: MenuItemSerializer})
    def post(self, request):
        data = request.data.copy()
        data['active'] = True
        serializer = MenuItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditOrDelete(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(request=MenuItemSerializer, responses={200: MenuItemSerializer})
    def patch(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk, active=True)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request={"id": "string"}, methods=["DELETE"])
    def delete(self, request, pk):
        menu_item = get_object_or_404(MenuItem, pk=pk, active=True)
        menu_item.active = False
        menu_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
