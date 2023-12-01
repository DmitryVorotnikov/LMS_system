from rest_framework.permissions import BasePermission


class CourseSetPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif view.action in ['create', 'destroy'] and request.user.is_staff:
            return False
        else:
            return True
