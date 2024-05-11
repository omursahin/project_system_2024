from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrDeny(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        else:
            return request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser
