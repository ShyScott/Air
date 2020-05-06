from rest_framework import serializers

from tcas.models import Team, User
from .user import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.exclude(student_profile=None).all())

    class Meta:
        model = Team
        fields = ['id', 'name', 'is_locked', 'course', 'members', 'leader']
        read_only_fields = ['is_locked']

    def __init__(self, *args, **kwargs):
        with_member_detail = kwargs.pop('with_member_detail', False)
        super().__init__(*args, **kwargs)
        if with_member_detail:
            self.fields['members'] = UserSerializer(many=True)


class TeamFormNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'course']

    def validate(self, attrs):
        if self.context['request'].user.teams.filter(course=attrs['course']).exists():
            raise serializers.ValidationError('You are already in one team of the course!')
        return attrs


class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']


class TeamVoteLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'leader']

    def validate(self, attrs):
        team = self.instance
        if not team.is_locked:
            raise serializers.ValidationError('This team is not confirmed by the course instructor!')
        if team.leader is not None:
            raise serializers.ValidationError('This team already has a leader!')
        if not team.members.filter(pk=attrs['leader'].pk).exists():
            raise serializers.ValidationError('This leader is not in the team!')
        return attrs
