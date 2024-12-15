from rest_framework.permissions import BasePermission

class IsDealer(BasePermission):
    """
    Permiso que permite el acceso solo a usuarios con el rol 'dealer'.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'dealer'