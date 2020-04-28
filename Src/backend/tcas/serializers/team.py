from rest_framework import serializers

from tcas.models import Team, User


class TeamSerializer(serializers.ModelSerializer):
    leader = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


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
