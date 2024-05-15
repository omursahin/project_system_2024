from rest_framework.permissions import BasePermission


class SpecialPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass

    def has_permission(self, request, view):
        pass
