from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from tcas.models import Course
from tcas.serializers import CourseSerializer, CourseListSerializer, CourseRemoveStudentSerializer
from tcas.permissions import IsTeacher, IsLogin


class CourseViewSet(ModelViewSet):

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.all()
        if self.request.user.is_teacher:
            return self.request.user.courses_teach
        return self.request.user.courses_in

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        elif self.action == 'remove_student':
            return CourseRemoveStudentSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsLogin()]
        return [IsTeacher()]

    @action(detail=True, methods=['post'])
    def remove_student(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseRemoveStudentSerializer(data=request.data, context={'course': course})
        serializer.is_valid(raise_exception=True)

        course.students.remove(serializer.data['user'])
        return Response(status=status.HTTP_204_NO_CONTENT)
