from rest_framework import serializers

from tcas.models import Team, User, TeamMember
from .user import UserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.objects.exclude(student_profile=None).all())
    voted_for = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'is_locked', 'course', 'members', 'leader', 'voted_for']
        read_only_fields = ['is_locked']

    def get_voted_for(self, team):
        try:
            team_member = TeamMember.objects.get(user=self.context['request'].user, team=team)
            return team_member.vote.pk if team_member.vote is not None else None
        except (KeyError, TeamMember.DoesNotExist):
            return None


class TeamDetailSerializer(TeamSerializer):
    """
    Read-only serializer to get team information with detail of members
    """
    members = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'is_locked', 'course', 'members', 'leader', 'voted_for']


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


class TeamLeaderBonusSerializer(serializers.Serializer):
    bonus = serializers.ChoiceField([-2, -1, 0, 1, 2])
