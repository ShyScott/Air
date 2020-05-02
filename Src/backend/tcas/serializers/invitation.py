from rest_framework import serializers

from tcas.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    """
    Serializer to list, retrieve and create invitations
    """

    inviter = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

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

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status == 1:
            instance.team.members.add(instance.invitee)
        return instance
