from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django_filters import rest_framework as filters

from .generic import PermissionDictMixin
from tcas.models import Team
from tcas.serializers import TeamSerializer, TeamNameSerializer
from tcas.permissions import IsTeacher, IsInCurrentCourse, IsInCurrentTeam


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
        'rename': [IsTeacher | IsInCurrentCourse],
        'quit': [IsTeacher | IsInCurrentTeam],
    }

    @action(detail=False, methods=['post'], serializer_class=TeamSerializer)
    def form_new(self, request, *arg, **kwargs):
        """
        Form a new team (for students)
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        if user.teams.filter(course=serializer.validated_data['course']).exists():
            raise ValidationError('You are already in one team of the course!')

        team = serializer.save()
        team.members.add(user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'], serializer_class=TeamNameSerializer)
    def rename(self, request, *arg, **kwargs):
        team = self.get_object()
        serializer = self.get_serializer(team, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def quit(self, request, *arg, **kwargs):
        team = self.get_object()
        team.students.remove(request.user)
        dismissed = False
        if team.students.count() == 0:
            dismissed = True
            team.delete()
        return Response({'dismiss': dismissed})
