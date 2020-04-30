from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .generic import PermissionDictMixin
from tcas.models import Course, Team
from tcas.serializers import CourseSerializer, CourseListSerializer, CourseRemoveStudentSerializer, TeamSerializer
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


class CourseViewSet(PermissionDictMixin, ModelViewSet):
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
        if self.action == 'list':
            return CourseListSerializer
        elif self.action == 'remove_student':
            return CourseRemoveStudentSerializer
        elif self.action == 'generate_teams':
            return TeamSerializer
        return CourseSerializer

    @action(detail=True, methods=['post'])
    def remove_student(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = CourseRemoveStudentSerializer(data=request.data, context={'course': course})
        serializer.is_valid(raise_exception=True)

        course.students.remove(serializer.data['user'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def generate_teams(self, request, *arg, **kwargs):
        course = self.get_object()
        form_method = course.form_method

        # Edge cases
        if course.form_method is None:
            raise ValidationError('Form method is not yet chosen!')
        if course.students.count() == 0:
            raise ValidationError('No student in this course!')

        # Initialize variables for further uses
        x = course.member_count_primary
        x_num = course.team_count_primary
        y = course.member_count_secondary
        y_num = course.team_count_secondary
        team_nums = [x for _ in range(x_num)]
        team_nums.extend([y for _ in range(y_num)])
        students = list(course.students.all())
        random.shuffle(students)
        min_gpa = max_gpa = 0

        if form_method == 3 or form_method == 5:
            mean_gpa = sum([user.student_profile.gpa for user in students]) / len(students)
            min_gpa = mean_gpa - course.floating_band
            max_gpa = mean_gpa + course.floating_band

        # Clean all system-generated teams first
        course.teams.filter(is_generated=True).delete()

        # Form method 1: all teams are created by students themselves
        if course.form_method == 1:
            teams = course.teams.all()

        # Form method 2, 3: random generation (3 with GPA optimization)
        elif course.form_method == 2 or course.form_method == 3:
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
                if pair.count() != 2:
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
                team = Team.objects.create(name='Team %d' % (index + 1), course=course, is_generated=True)
                team.members.set(members_list[index])
                teams.append(team)

        return Response(TeamSerializer(teams, many=True).data)
