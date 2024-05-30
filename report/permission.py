from rest_framework import permissions


class IsAuthenticatedForCreate(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to create objects.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return False
