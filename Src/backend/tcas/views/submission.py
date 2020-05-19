from rest_framework.viewsets import ModelViewSet

from django_filters import rest_framework as filters

from .generic import PermissionDictMixin
from tcas.models import Submission
from tcas.serializers import SubmissionSerializer
from tcas.permissions import IsTeacher, IsInCurrentCourse


class SubmissionFilter(filters.FilterSet):
    class Meta:
        model = Submission
        fields = ['course']


class SubmissionViewSet(PermissionDictMixin, ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filterset_class = SubmissionFilter
    permission_dict = {
        'list': [IsTeacher | IsInCurrentCourse],
        'retrieve': [IsTeacher | IsInCurrentCourse],
        'others': [IsTeacher],
    }
