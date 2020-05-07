from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django_filters import rest_framework as filters

from .generic import PermissionDictMixin
from tcas.models import User, Team, TeamMember
from tcas.serializers import TeamSerializer, TeamNameSerializer, TeamFormNewSerializer, TeamVoteLeaderSerializer
from tcas.permissions import IsTeacher, IsInCurrentCourse, IsInCurrentTeam

from django.db.models import Count


class TeamFilter(filters.FilterSet):
    class Meta:
        model = Team
        fields = ['course']


class TeamViewSet(PermissionDictMixin, ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filterset_class = TeamFilter
    permission_dict = {
        'list': [IsTeacher | IsInCurrentCourse],
        'retrieve': [IsTeacher | IsInCurrentCourse],
        'create': [IsTeacher],
        'update': [IsTeacher],
        'partial_update': [IsTeacher],
        'destroy': [IsTeacher],
        'form_new': [IsInCurrentCourse],
        'rename': [IsTeacher | IsInCurrentTeam],
        'quit': [IsTeacher | IsInCurrentTeam],
        'vote_leader': [IsInCurrentTeam],
    }

    @action(detail=False, methods=['post'], serializer_class=TeamFormNewSerializer)
    def form_new(self, request, *arg, **kwargs):
        """
        Form a new team (for students)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        team = serializer.save()
        team.members.add(request.user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'], serializer_class=TeamNameSerializer)
    def rename(self, request, *arg, **kwargs):
        team = self.get_object()
        serializer = self.get_serializer(team, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def quit(self, request, *arg, **kwargs):
        team = self.get_object()
        if team.is_locked:
            raise ValidationError('This team is already confirmed and locked by the course instructor!')
        team.members.remove(request.user)
        dismissed = False
        if team.members.count() == 0:
            dismissed = True
            team.delete()
        return Response({'dismiss': dismissed})

    @action(detail=True, methods=['patch'], serializer_class=TeamVoteLeaderSerializer)
    def vote_leader(self, request, *arg, **kwargs):
        team = self.get_object()
        serializer = self.get_serializer(team, data=request.data)
        serializer.is_valid(raise_exception=True)
        team_members = TeamMember.objects.filter(team=team)
        team_members.filter(user=request.user).update(vote=serializer.validated_data['leader'])

        # Check if all members have voted
        if not team_members.filter(vote__isnull=True).exists():
            leader_pk = team_members.values('vote').annotate(vote_count=Count('vote')).order_by('-vote_count').first()['vote']
            team.leader = User.objects.get(pk=leader_pk)
            team.save()

        return Response(serializer.data)
