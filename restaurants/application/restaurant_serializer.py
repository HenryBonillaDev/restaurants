from rest_framework import serializers
from restaurants.domain.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'rating', 'status', 'category', 'latitude', 'longitude'
        ]
