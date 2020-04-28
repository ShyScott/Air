from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from rest_framework.response import Response

from django.contrib.auth import update_session_auth_hash

from django.db.models import Value, Q
from django.db.models.functions import Length, Replace

from django_filters import rest_framework as filters

from .generic import PermissionDictMixin
from tcas.models import User, Course, Team
from tcas.serializers import UserSerializer, ChangePasswordSerializer, StudentBatchCreateSerializer, StudentBatchCreateWeakSerializer
from tcas.permissions import IsTeacher, IsLogin, IsCurrentUser, IsInCurrentCourse


class UserFilter(filters.FilterSet):
    username = filters.CharFilter(method='filter_username')
    course = filters.ModelChoiceFilter(field_name='courses_in', queryset=Course.objects.all())

    class Meta:
        model = User
        fields = ['username', 'course']

    def filter_username(self, queryset, field_name, value):
        return queryset.filter(username__icontains=value).order_by(Length(Replace('username', Value(value))))


def filter_duplicated_user(duplicated_users):
    """
    Find duplicated user according to user_data, and store the duplications into duplicated_users
    """
    def is_duplicated_user(user_data):
        try:
            duplicated_user = User.objects.get(
                Q(username=user_data['username']) |
                Q(student_profile__student_id=user_data['student_profile']['student_id']) |
                Q(student_profile__email=user_data['student_profile']['email']))
        except User.DoesNotExist:
            return True
        duplicated_users.append(duplicated_user)
        return False

    return is_duplicated_user


class UserViewSet(PermissionDictMixin, ModelViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilter
    permission_dict = {
        'list': [IsTeacher | IsInCurrentCourse],
        'retrieve': [IsLogin],
        'create': [IsTeacher, IsInCurrentCourse],
        'me': [IsLogin],
        'change_password': [IsCurrentUser],
        'others': [IsTeacher],
    }

    def get_serializer_class(self):
        if self.action == 'create':
            return StudentBatchCreateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'me':
            context['full_info'] = True
        return context

    def create(self, request, *args, **kwargs):
        serializer = StudentBatchCreateWeakSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Find and remove duplicated students from serializer
        duplicated_users = []
        filtered_users_data = list(filter(filter_duplicated_user(duplicated_users), serializer.data['students']))
        filtered_data = serializer.data.copy()
        filtered_data['students'] = filtered_users_data
        serializer = self.get_serializer(data=filtered_data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Add duplicated students into the course
        serializer.validated_data['course'].students.add(*duplicated_users)

        duplicated_users_serializer = UserSerializer(duplicated_users, many=True, context={'request': request})
        headers = self.get_success_headers(serializer.validated_data)
        return Response(
            {'duplications': duplicated_users_serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            raise ValidationError('Wrong old password')
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        # Refresh token for current user
        if user == request.user:
            update_session_auth_hash(request, user)
        return Response(status=status.HTTP_204_NO_CONTENT)
