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
