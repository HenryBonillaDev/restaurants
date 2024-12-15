from rest_framework.exceptions import ValidationError
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    actual_pass = serializers.CharField(write_only=True)
    new_pass = serializers.CharField(write_only=True)
    confirm_new_pass = serializers.CharField(write_only=True)

    def validate(self, attrs):
        actual_pass = attrs.get("actual_pass")
        new_pass = attrs.get("new_pass")
        confirm_new_pass = attrs.get("confirm_new_pass")
        user = self.context.get("request").user

        if not user.check_password(actual_pass):
            raise ValidationError("La contraseña actual es incorrecta.")

        if new_pass != confirm_new_pass:
            raise ValidationError("Las contraseñas nuevas no coinciden.")

        if len(new_pass) < 8:
            raise ValidationError("La contraseña nueva es muy corta")

        return attrs
