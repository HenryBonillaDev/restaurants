from django_filters import rest_framework as filters
from orders.domain.models import Order

class OrderFilter(filters.FilterSet):
    customer = filters.UUIDFilter(field_name='customer__id')
    restaurant = filters.UUIDFilter(field_name='restaurant__id')
    status = filters.CharFilter(lookup_expr='iexact')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    total_min = filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_max = filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    address_contains = filters.CharFilter(field_name='delivery_address', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = [
            'customer', 
            'restaurant', 
            'status', 
            'created_after', 
            'created_before', 
            'total_min', 
            'total_max', 
            'address_contains'
        ]
