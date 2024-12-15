import django_filters
from restaurants.domain.models import Restaurant

class RestaurantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    rating_max = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    category = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'rating_min', 'rating_max']
