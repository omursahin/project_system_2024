from rest_framework.permissions import BasePermission


class IsAdminOrUserCanRead(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user or request.user.is_staff)
        else:
            return bool(request.user and request.user.is_staff)
