from rest_framework.permissions import BasePermission

class AllowCreateUpdateOrRestAuthenticated(BasePermission):
    """
    Permite:
    - create, update e partial_update para qualquer um
    - resto, apenas se for autenticado
    - bloqueia destroy
    """
    def has_permission(self, request, view):
        if view.action in ['create', 'update', 'partial_update']:
            return True
        else:
            return request.user and request.user.is_authenticated
