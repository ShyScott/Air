from rest_framework import serializers

from tcas.models import Invitation
from .course import CourseReadOnlySerializer


class InvitationSerializer(serializers.ModelSerializer):
    """
    Serializer to list, retrieve and create invitations
    """

    course = CourseReadOnlySerializer(source='team.course', read_only=True)

    class Meta:
        model = Invitation
        fields = '__all__'
        read_only_fields = ['inviter', 'invite_time', 'status']

    def validate(self, attrs):
        course = attrs['team'].course
        invitee = attrs['invitee']
        if not invitee.courses_in.filter(pk=course.pk).exists():
            raise serializers.ValidationError('The invitee is not in the course!')
        if invitee.teams.filter(course=course).exists():
            raise serializers.ValidationError('The invitee is already in one team of the course!')
        if Invitation.objects.filter(team=attrs['team'], invitee=invitee, status=0).exists():
            raise serializers.ValidationError('The invitee is already invited by one of your team members!')
        return attrs


class InvitationResponseSerializer(serializers.ModelSerializer):
    """
    Serializer to respond an invitation
    """

    status = serializers.ChoiceField([-1, 1])

    class Meta:
        model = Invitation
        fields = ['status']

    def validate(self, attrs):
        if self.instance.status != 0:
            raise serializers.ValidationError('The invitation was already responded!')
        return attrs
