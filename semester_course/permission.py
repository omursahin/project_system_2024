from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrDeny(BasePermission):
    """
    Custom permission to only allow admin users to edit semester courses.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser
