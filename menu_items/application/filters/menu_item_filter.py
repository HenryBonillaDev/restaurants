from django_filters import rest_framework as filters
from menu_items.domain.models import MenuItem

class MenuItemFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category = filters.CharFilter(lookup_expr='icontains')
    restaurant_id = filters.UUIDFilter(field_name='restaurant__id')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'restaurant_id', 'price_min', 'price_max', 'available']
