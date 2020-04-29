from rest_framework import serializers

from django.contrib.auth.hashers import make_password

from tcas.models import User, StudentProfile, Course


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve and update student profiles
    """
    gpa = serializers.FloatField(min_value=0, max_value=4, required=False)

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'email', 'gpa']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to list and delete one user
    """

    student_profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'student_profile']

    # def create(self, validated_data: dict):
    #     profile_data = validated_data.pop('student_profile')
    #     user = super().create(validated_data)
    #     user.set_password(self.context['password'])
    #     user.save()
    #     StudentProfile.objects.create(**profile_data)
    #     return user

    def to_representation(self, instance):
        """
        Control the representation according to current user's role
        """
        rep = super().to_representation(instance)
        if self.context.get('full_info') is None and not self.context['request'].user.is_teacher:
            rep.pop('student_profile')
        return rep


class StudentBatchCreateSerializer(serializers.Serializer):
    """
    Serializer to batch create students
    """

    students = UserSerializer(many=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    default_password = serializers.CharField()

    def create(self, validated_data):
        users = []
        for user_data in validated_data['students']:
            profile_data = user_data.pop('student_profile')
            user = User.objects.create(**user_data)
            StudentProfile.objects.create(user=user, **profile_data)
            user.set_password(validated_data['default_password'])
            user.save()
            users.append(user)

        validated_data['course'].students.add(*users)
        return users


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to change an user's password
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class StudentProfileWeakSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=64)
    email = serializers.EmailField(max_length=254)
    gpa = serializers.FloatField(min_value=0, max_value=4, required=False)


class UserWeakSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    student_profile = StudentProfileWeakSerializer()


class StudentBatchCreateWeakSerializer(serializers.Serializer):
    students = UserWeakSerializer(many=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    default_password = serializers.CharField()
