from rest_framework import serializers
from users.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Debe contener al menos 8 caracteres."
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'role', 
            'first_name', 'last_name', 'phone', 'default_address', 'restaurant'
        ]
        extra_kwargs = {
            'email': {'help_text': 'Correo electrónico único del usuario.'},
            'role': {'help_text': 'Rol del usuario: dealer o customer.'},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role=validated_data['role'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            default_address=validated_data.get('default_address', ''),
            restaurant=validated_data.get('restaurant', None),
        )
        return user
