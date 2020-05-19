from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from rest_framework.response import Response

from django.contrib.auth import update_session_auth_hash

from django.db.models import Value, Q, Case, When
from django.db.models.functions import Length, Replace, Least

from django_filters import rest_framework as filters

from .generic import PermissionDictMixin
from tcas.models import User, Course, StudentProfile
from tcas.serializers import UserSerializer, ChangePasswordSerializer, StudentBatchCreateSerializer, UserAvatarSerializer
from tcas.permissions import IsTeacher, IsLogin, IsInCurrentCourse


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    course = filters.ModelChoiceFilter(field_name='courses_in', queryset=Course.objects.all())

    class Meta:
        model = User
        fields = ['search', 'course']

    def filter_search(self, queryset, field_name, value):
        max_length = 999999
        return queryset.filter(
            Q(username__icontains=value) | Q(student_profile__student_id__icontains=value)
        ).annotate(
            username_length=Case(
                When(username__icontains=value, then=Length(Replace('username', Value(value)))),
                default=Value(max_length),
            ),
        ).annotate(
            student_id_length=Case(
                When(student_profile__student_id__icontains=value, then=Length(Replace('student_profile__student_id', Value(value)))),
                default=Value(max_length),
            ),
        ).order_by(Least('username_length', 'student_id_length'))


class UserViewSet(PermissionDictMixin, ModelViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilter
    permission_dict = {
        'list': [IsTeacher | IsInCurrentCourse],
        'retrieve': [IsLogin],
        'create': [IsTeacher, IsInCurrentCourse],
        'me': [IsLogin],
        'change_password': [IsLogin],
        'avatar': [IsLogin],
        'others': [IsTeacher],
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentBatchCreateSerializer
        if self.action == 'change_password':
            return ChangePasswordSerializer
        if self.action == 'avatar':
            return UserAvatarSerializer
        return UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['with_student_gpa'] = self.request.user.is_authenticated and (
            self.action == 'me' or (self.action in ['list', 'retrieve'] and self.request.user.is_teacher))
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = serializer.validated_data['course']
        password = serializer.validated_data['default_password']

        # Find and remove duplicated students, and create User instance for others
        duplicated_users = []
        multiple_exist_users = []
        course_add_users = []
        for user_raw in serializer.validated_data['students']:
            user_data = user_raw.copy()
            try:
                user = User.objects.get(
                    Q(student_profile__student_id=user_data['student_profile']['student_id']) |
                    Q(student_profile__email=user_data['student_profile']['email']))
                duplicated_users.append(user)
            except User.DoesNotExist:
                profile_data = user_data.pop('student_profile')
                user = User.objects.create(email=profile_data['email'], **user_data)
                StudentProfile.objects.create(user=user, **profile_data)
                user.set_password(password)
                user.save()
            except User.MultipleObjectsReturned:
                multiple_exist_users.append(user_data)
                continue
            course_add_users.append(user)

        course.students.add(*course_add_users)

        # Clear form_method and related properties of the course
        course.clear_forming_options()

        duplicated_users_serializer = UserSerializer(duplicated_users, many=True, context={'with_student_gpa': True})
        return Response(
            {
                'added_students_count': len(course_add_users),
                'duplications': duplicated_users_serializer.data,
                'multiple_existings': multiple_exist_users,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def change_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        # Refresh token for current user
        if user == request.user:
            update_session_auth_hash(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'])
    def avatar(self, request, *arg, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
