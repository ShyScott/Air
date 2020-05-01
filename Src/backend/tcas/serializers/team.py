from rest_framework import serializers

from tcas.models import Team, User


class TeamSerializer(serializers.ModelSerializer):
    is_locked = serializers.BooleanField(read_only=True)
    leader = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.exclude(student_profile=None).all())

    class Meta:
        model = Team
        fields = ['id', 'name', 'is_locked', 'course', 'members', 'leader']


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class TeamInviteSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_user(self, user):
        course = self.context['course']
        if not course.students.filter(pk=user.pk).exists():
            raise serializers.ValidationError('This user is not in the course!')
        if user.teams.filter(course=course).exists():
            raise serializers.ValidationError('This user is already in one team of the course!')
        return user
