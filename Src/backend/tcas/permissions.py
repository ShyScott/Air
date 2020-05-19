from rest_framework.permissions import BasePermission, IsAuthenticated as IsLogin

from .models import Course, Team


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.__class__.__name__ == 'User':
            return obj == request.user
        return False


class IsInCurrentCourse(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.__class__.__name__ == 'CourseViewSet':
            return True
        course_pk = request.query_params.get('course') or request.data.get('course')
        if course_pk is not None:
            try:
                course = Course.objects.get(pk=course_pk)
            except Course.DoesNotExist:
                return False
            return course.instructor == request.user or course.students.filter(pk=request.user.pk).exists()
        return False


class IsInCurrentTeam(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if view.__class__.__name__ == 'TeamViewSet':
            return True
        team_pk = request.query_params.get('team') or request.data.get('team')
        if team_pk is None:
            return False
        return request.user.teams.filter(pk=team_pk).exists()

    def has_object_permission(self, request, view, obj):
        if obj.__class__.__name__ == 'Team':
            return obj.members.filter(pk=request.user.pk).exists()
        return True
