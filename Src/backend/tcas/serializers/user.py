from rest_framework import serializers

from tcas.models import User, StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve and update student profiles
    """

    class Meta:
        model = StudentProfile
        fields = ['student_id', 'email', 'gpa']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer to create, list and delete students
    """

    password = serializers.CharField(write_only=True, required=True)
    student_profile = StudentProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'student_profile']

    def create(self, validated_data: dict):
        profile_data = validated_data.pop('student_profile')
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        profile = StudentProfile(user=user, **profile_data)
        profile.save()
        return user


class StudentBatchSerializer(serializers.Serializer):
    """
    Serializer to batch create students
    """

    students = StudentSerializer(many=True)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve and update user profiles
    """

    class Meta:
        model = User
        fields = ['id', 'username']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer to change an user's password
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
