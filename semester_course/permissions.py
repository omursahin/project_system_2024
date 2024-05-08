from rest_framework.permissions import BasePermission


class IsAdminOrDeny(BasePermission):
    """
    Custom permission to only allow admin users to edit semester courses.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
