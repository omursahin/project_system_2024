from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows access only to owner.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj
