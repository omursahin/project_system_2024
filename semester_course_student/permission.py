from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminAllPermissionAndStudentSafeMethod(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        elif request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        else:
            return False