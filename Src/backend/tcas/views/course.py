from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from django_filters import rest_framework as filters

from django.db.models import Value
from django.db.models.functions import Length, Replace

from .generic import PermissionDictMixin
from tcas.models import Course, Team
from tcas.serializers import (
    CourseSerializer,
    CourseReadOnlySerializer,
    CourseRemoveStudentSerializer,
    CourseCreateSerializer,
    TeamSerializer,
    UserSerializer,
)
from tcas.permissions import IsTeacher, IsLogin

import random


def group_students(students, members_list, team_nums, current_student, current_team, gpa_optimized, min_gpa, max_gpa):
    # Exit
    if current_student == len(students):
        while len(members_list[-1]) == 0:
            members_list.pop()
        return True

    # Select a student (pair) and push into current team
    for index in range(current_student, len(students)):
        if isinstance(students[index], list):
            count = len(students[index])
            members_list[current_team].extend(students[index])
        else:
            count = 1
            members_list[current_team].append(students[index])

        has_new_team = len(members_list[current_team]) == team_nums[current_team]
        if has_new_team:
            # Check the GPA of this team if necessary
            if gpa_optimized:
                gpa = sum(member.student_profile.gpa for member in members_list[current_team]) / team_nums[current_team]
                if gpa < min_gpa or gpa > max_gpa:
                    for _ in range(count):
                        members_list[current_team].pop()
                    continue

            members_list.append([])
            current_team += 1

        if group_students(students, members_list, team_nums, current_student + 1, current_team, gpa_optimized, min_gpa, max_gpa):
            return True

        if has_new_team:
            members_list.pop()
            current_team -= 1
        for _ in range(count):
            members_list[current_team].pop()

    # No satisfying solution, reject
    return False


class CourseFilter(filters.FilterSet):
    title = filters.CharFilter(method='filter_title')

    class Meta:
        model = Course
        fields = ['title']

    def filter_title(self, queryset, field_name, value):
        return queryset.filter(title__icontains=value).order_by(Length(Replace('title', Value(value))))


class CourseViewSet(PermissionDictMixin, ModelViewSet):
    filterset_class = CourseFilter
    permission_dict = {
        'list': [IsLogin],
        'retrieve': [IsLogin],
        'others': [IsTeacher],
    }

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Course.objects.all()
        if self.request.user.is_teacher:
            return Course.objects.filter(instructor=self.request.user)
        return Course.objects.filter(students=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseReadOnlySerializer
        elif self.action == 'create':
            return CourseCreateSerializer
        elif self.action == 'remove_student':
            return CourseRemoveStudentSerializer
        elif self.action in ['generate_teams', 'confirm_teams']:
            return TeamSerializer
        elif self.action == 'single_students':
            return UserSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'])
    def remove_student(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseRemoveStudentSerializer(data=request.data, context={'course': course})
        serializer.is_valid(raise_exception=True)

        course.students.remove(serializer.data['user'])

        # Clear form_method and related fields because student number is changed
        course.clear_forming_options()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def generate_teams(self, request, *arg, **kwargs):
        course = self.get_object()
        form_method = course.form_method

        # Edge cases
        if form_method is None:
            raise ValidationError('Form method is not yet chosen!')
        if course.students.count() == 0:
            raise ValidationError('No student in this course!')

        # Initialize variables for further uses
        team_nums = course.team_nums
        students = list(course.students.all())
        random.shuffle(students)
        min_gpa = max_gpa = 0

        if form_method in [3, 5]:
            mean_gpa = course.mean_gpa
            min_gpa = mean_gpa - course.floating_band
            max_gpa = mean_gpa + course.floating_band

        # Form method 1: all teams are created by students themselves
        if form_method == 1:
            teams = TeamSerializer(course.teams.all(), many=True).data

        # Form method 2, 3: random generation (3 with GPA optimization)
        elif form_method in [2, 3]:
            members_list = [[]]

            # Try to group all students. This may fail because of GPA optimization (too small floating bands)
            if not group_students(students, members_list, team_nums, 0, 0, form_method == 3, min_gpa, max_gpa):
                raise ValidationError('GPA floating band is too small!')

        # Form method 4, 5: random combination from pairs of students (5 with GPA optimization)
        else:
            # Validate whether all the students is in pairs
            pairs_list = [list(team.members.all()) for team in course.teams.all()]
            random.shuffle(pairs_list)
            total = 0
            for pair in pairs_list:
                if len(pair) != 2:
                    raise ValidationError('There exist teams which are not pairs of students!')
                total += 2
            if total != course.students.count():
                raise ValidationError('There exist students which are not in any team!')
            members_list = [[]]

            # Try to group pairs of students. This may fail because of GPA optimization (too small floating bands)
            if not group_students(students, members_list, team_nums, 0, 0, form_method == 5, min_gpa, max_gpa):
                raise ValidationError('GPA floating band is too small!')

        # Create teams from members_list for method 2, 3, 4, 5
        if form_method != 1:
            teams = []
            for index in range(len(members_list)):
                # team = Team.objects.create(name='Team %d' % (index + 1), course=course, is_generated=True)
                # team.members.set(members_list[index])
                # teams.append(team)
                teams.append({
                    'name': 'Team %d' % (index+1),
                    'course': course.pk,
                    'members': UserSerializer(members_list[index], many=True, context={'with_profile_detail': True}).data,
                })

        return Response(teams)

    @action(detail=True, methods=['get'])
    def single_students(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = UserSerializer(course.students.exclude(teams__course=course).all(), many=True, context={'with_profile_detail': True})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm_teams(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        # Validate all teams and team members
        teams = serializer.validated_data
        team_nums = course.team_nums
        students = list(course.students.all())

        for team in teams:
            members = team['members']
            count = len(members)
            if count not in team_nums:
                raise ValidationError('There are teams that do not meet the forming requirements!')
            team_nums.remove(count)

            for member in members:
                if member not in students:
                    raise ValidationError('There are students that are in multiple teams, or are not in this course!')
                students.remove(member)

        if len(team_nums) > 0:
            raise ValidationError('There are too few teams!')
        if len(students) > 0:
            raise ValidationError('There are too few students! (This may be a bug)')

        # Remove all existing teams
        course.teams.all().delete()

        # Create teams
        confirmed_teams = []
        for team_data in teams:
            team_raw = team_data.copy()
            team_raw['course'] = course
            members = team_raw.pop('members')
            confirmed_team = Team.objects.create(is_locked=True, **team_raw)
            confirmed_team.members.set(members)
            confirmed_teams.append(confirmed_team)

        course.is_confirmed = True
        course.save()

        return Response(TeamSerializer(confirmed_teams, many=True).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def mean_gpa(self, request, *args, **kwargs):
        course = self.get_object()
        return Response({'mean_gpa': course.mean_gpa})
