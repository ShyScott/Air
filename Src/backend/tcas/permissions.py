from rest_framework.permissions import BasePermission, IsAuthenticated as IsLogin


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher

    def has_object_permission(self, request, view, obj):
        return request.user.is_teacher


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.__class__.__name__ == 'User':
            return obj == request.user
        return False
