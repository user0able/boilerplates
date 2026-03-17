from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Solo permite acceso al propietario del objeto."""

    def has_object_permission(self, request, view, obj):
        return obj == request.user or (hasattr(obj, "user") and obj.user == request.user)
