from rest_framework import serializers

from tcas.models import User, StudentProfile, Course

from versatileimagefield.serializers import VersatileImageFieldSerializer


class WeakValidationMixin:
    """
    Mixin with overrode `__init__` and `include_extra_kwargs` methods
    to remove UniqueValidators with parameter `weak=True`.
    """

    def __init__(self, *args, **kwargs):
        self.weak = kwargs.pop('weak', False)
        super().__init__(*args, **kwargs)

    def include_extra_kwargs(self, kwargs, extra_kwargs):
        ret = super().include_extra_kwargs(kwargs, extra_kwargs)
        if self.weak and ret.get('validators') is not None:
            new_validators = []
            for validator in ret['validators']:
                if type(validator).__name__ != 'UniqueValidator':
                    new_validators.append(validator)
            ret['validators'] = new_validators
        return ret


class StudentProfileSerializer(WeakValidationMixin, serializers.ModelSerializer):
    """
    Serializer to retrieve and update student profiles
    """

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'email', 'gpa']
        extra_kwargs = {
            'gpa': {'min_value': 0, 'max_value': 4},
        }


class UserSerializer(WeakValidationMixin, serializers.ModelSerializer):
    """
    Serializer to list and delete one user
    """
    avatar = VersatileImageFieldSerializer(sizes='user_avatar')

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'student_profile']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student_profile'] = StudentProfileSerializer(weak=self.weak)

    def to_representation(self, instance):
        """
        Control the representation according to current user's role
        """
        rep = super().to_representation(instance)
        if not self.context.get('with_student_gpa', False) and rep['student_profile'] is not None:
            rep['student_profile'].pop('gpa')
        return rep


class StudentBatchCreateSerializer(serializers.Serializer):
    """
    Serializer to batch create students
    """

    students = UserSerializer(many=True, weak=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    default_password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to change an user's password
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer to update user's avatar
    """
    avatar = VersatileImageFieldSerializer(sizes='user_avatar')

    class Meta:
        model = User
        fields = ['id', 'avatar']
