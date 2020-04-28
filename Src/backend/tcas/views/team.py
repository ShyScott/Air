from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .generic import PermissionDictMixin
from tcas.models import Team
from tcas.serializers import TeamSerializer, TeamNameSerializer
from tcas.permissions import IsTeacher, IsInCurrentCourse, IsInCurrentTeam


class TeamViewSet(PermissionDictMixin, ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_dict = {
        'list': [IsTeacher | IsInCurrentCourse],
        'retrieve': [IsTeacher | IsInCurrentCourse],
        'create': [IsTeacher | IsInCurrentCourse],
        'update': [IsTeacher],
        'partial_update': [IsTeacher],
        'destroy': [IsTeacher],
        'rename': [IsTeacher | IsInCurrentCourse],
        'quit': [IsTeacher | IsInCurrentTeam],
    }

    def perform_create(self, serializer):
        user = self.request.user
        if user.teams.filter(course=serializer.data['course']).exists():
            raise ValidationError('This user is already in one team of the course!')
        team = serializer.save()
        team.members.add(self.request.user)

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
