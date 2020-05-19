from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import mixins

from tcas.models import Invitation, Course
from tcas.serializers import InvitationSerializer, InvitationResponseSerializer, InvitationDetailSerializer
from tcas.permissions import IsLogin, IsInCurrentTeam
from .generic import PermissionDictMixin

from django.db.models import Q

from django_filters import rest_framework as filters


class InvitationFilter(filters.FilterSet):
    inviter = filters.BooleanFilter(method='filter_role')
    invitee = filters.BooleanFilter(method='filter_role')
    course = filters.ModelChoiceFilter(field_name='team__course', queryset=Course.objects.all())

    class Meta:
        model = Invitation
        fields = ['inviter', 'invitee', 'course']

    def filter_role(self, queryset, field_name, value):
        return queryset.filter(**{field_name: self.request.user}) if value else queryset


class InvitationViewSet(
    PermissionDictMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    filterset_class = InvitationFilter
    permission_dict = {
        'create': [IsInCurrentTeam],
        'others': [IsLogin],
    }

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Invitation.objects.all()
        return Invitation.objects.filter(Q(inviter=self.request.user) | Q(invitee=self.request.user))

    def get_serializer_class(self):
        if self.action == 'create':
            return InvitationSerializer
        if self.action == 'respond':
            return InvitationResponseSerializer
        return InvitationDetailSerializer

    def perform_create(self, serializer):
        serializer.save(inviter=self.request.user)

    @action(detail=True, methods=['put'])
    def respond(self, request, *args, **kwargs):
        invitation = self.get_object()
        if invitation.invitee != request.user:
            raise PermissionDenied()

        serializer = self.get_serializer(invitation, data=request.data)
        serializer.is_valid(raise_exception=True)
        invitation = serializer.save()
        team = invitation.team
        course = team.course
        if invitation.status == 1:
            team.members.add(request.user)
            # Mark all un-answered invitations from other teams in the same course as the current team as 'outdated'
            Invitation.objects.filter(team__course=course, invitee=request.user, status=0).update(status=-2)

            # If form method in [4, 5] and current team is already a pair, mark all un-answered invitations from this team as 'outdated'
            if course.form_method in [4, 5] and team.members.count() >= 2:
                Invitation.objects.filter(team=team, status=0).update(status=-2)

            Invitation.objects.filter()

        return Response(serializer.data)
