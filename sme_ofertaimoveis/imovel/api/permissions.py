from rest_framework.permissions import BasePermission

class AllowOnlyCreateUpdate(BasePermission):
    def has_permission(self, request, view):
        return view.action in ['create', 'update', 'partial_update']
