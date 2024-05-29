from rest_framework.permissions import BasePermission

from group.models import Group
from semester_course.models import SemesterCourse


class SpecialPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass

    def has_permission(self, request, view):
        pass



class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admin kullanıcılar her şeye erişebilir
        if request.user.is_admin:
            return True
        # Sadece grup sahibi erişebilir
        return obj.owner == request.user

