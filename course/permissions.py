from rest_framework.permissions import BasePermission


class IsAdminOrUserCanRead(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return bool(request.user.is_authenticated or request.user.is_staff)
        else:
            return bool(request.user.is_authenticated and request.user.is_staff)
