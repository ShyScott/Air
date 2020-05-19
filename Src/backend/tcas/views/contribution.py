from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from tcas.models import Contribution, Team, TeamMember
from tcas.serializers import ContributionSerializer, ContributionCreateSerializer
from tcas.permissions import IsInCurrentTeam, IsLogin
from .generic import PermissionDictMixin

from django_filters import rest_framework as filters


class ContributionFilter(filters.FilterSet):
    team = filters.ModelChoiceFilter(field_name='team_member__team', queryset=Team.objects.all())

    class Meta:
        model = Contribution
        fields = ['submission', 'team']


class ContributionViewSet(PermissionDictMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Contribution.objects.all()
    pagination_class = None
    filterset_class = ContributionFilter
    permission_dict = {
        'list': [IsInCurrentTeam],
        'create': [IsLogin],  # Need to validate if current user is the team leader, which is validated in view function
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return ContributionSerializer
        return ContributionCreateSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validate if current user is the team leader
        team = serializer.validated_data[0]['team']
        if team.leader != request.user:
            raise PermissionDenied
        for item in serializer.validated_data:
            if team != item['team']:
                raise PermissionDenied

        contributions = []
        for item in serializer.validated_data:
            team_member = TeamMember.objects.get(team=team, user=item['member'])
            contribution, created = Contribution.objects.get_or_create(
                submission=item['submission'],
                team_member=team_member,
                defaults={'level': item['level']},
            )
            if not created:
                contribution.level = item['level']
                contribution.save()
            contributions.append(contribution)

        return Response(ContributionSerializer(contributions, many=True).data, status=status.HTTP_201_CREATED)
