from rest_framework import serializers

from tcas.models import Contribution, User, Submission, Team
from .user import UserSerializer


class ContributionSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(read_only=True, source='team_member.team')
    member = UserSerializer(source='team_member.user')

    class Meta:
        model = Contribution
        fields = ['id', 'submission', 'team', 'member', 'level']


class ContributionCreateSerializer(serializers.Serializer):
    submission = serializers.PrimaryKeyRelatedField(queryset=Submission.objects.all())
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    level = serializers.ChoiceField([0, 1, 2, 3])

    def validate(self, attrs):
        team = attrs['team']
        member = attrs['member']
        submission = attrs['submission']
        if not team.course.submissions.filter(pk=submission.pk).exists():
            raise serializers.ValidationError('This submission is not for the current course!')
        if not team.members.filter(pk=member.pk).exists():
            raise serializers.ValidationError('This member is not in the given team!')
        return attrs
