from rest_framework import serializers
from menu_items.domain.models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
