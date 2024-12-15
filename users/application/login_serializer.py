from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        print(f'Intentando autenticar con username: {username}, password: {password}')
        user = authenticate(username=username, password=password)
        
        if user:
            print(f'Usuario autenticado: {user}')
        else:
            print('Autenticación fallida')

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'role': user.role,
            }

        raise serializers.ValidationError('Invalid credentials')