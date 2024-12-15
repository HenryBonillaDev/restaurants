from rest_framework import serializers
from menu_items.domain.models import MenuItem
from orders.domain.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    menu_item = serializers.UUIDField()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'subtotal', 'notes']
        read_only_fields = ['subtotal']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'restaurant', 'status', 'total_amount', 
            'delivery_address', 'order_items'
        ]

    def validate(self, data):
        """
        Verificar que el `restaurant` de la orden coincida con el `restaurant` de todos los `order_items`.
        """
        restaurant = data.get('restaurant')
        order_items = data.get('order_items')

        for item in order_items:
            menu_item = MenuItem.objects.get(id=item['menu_item'])
            if menu_item.restaurant != restaurant:
                raise serializers.ValidationError(
                    f"El producto {menu_item.name} no pertenece al mismo restaurante de la orden."
                )

        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')

        order = Order.objects.create(**validated_data, total_amount=0)

        total_amount = 0
        for item_data in order_items_data:
            item_data['order'] = order
            
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            item_data['menu_item'] = menu_item
            
            subtotal = item_data['quantity'] * menu_item.price
            item_data['subtotal'] = subtotal
            OrderItem.objects.create(**item_data)
            total_amount += subtotal

        order.total_amount = total_amount
        order.save()

        return order
