from rest_framework import mixins, status
from rest_framework.serializers import ListSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from rest_framework.response import Response

from django.contrib.auth import update_session_auth_hash

from tcas.models import User
from tcas.serializers import StudentSerializer, UserSerializer, ChangePasswordSerializer, StudentBatchSerializer
from tcas.permissions import IsTeacher, IsLogin, IsCurrentUser


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSerializer
        return StudentSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'batch_create':
            kwargs['many'] = isinstance(kwargs.get('data'), list)
        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsLogin()]
        return [IsTeacher()]

    @action(
        detail=True,
        methods=['post'],
        serializer_class=ChangePasswordSerializer,
        permission_classes=[IsCurrentUser],
    )
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

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsTeacher],
    )
    def batch_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)
