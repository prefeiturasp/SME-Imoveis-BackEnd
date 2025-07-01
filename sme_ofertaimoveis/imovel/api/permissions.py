from rest_framework.permissions import BasePermission

class AllowCreateUpdateOrRestAuthenticated(BasePermission):
    """
    Permite:
    - create, update e partial_update para qualquer um
    - resto, apenas se for autenticado
    - bloqueia destroy
    """
    def has_permission(self, request, view):
        print(view.action)
        if view.action in ['create', 'update', 'partial_update', 'checa_iptu_ja_existe']:
            return True
        else:
            return request.user and request.user.is_authenticated
