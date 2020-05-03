from rest_framework import serializers

from tcas.models import Course, User, Team
from .team import TeamSerializer
from .user import UserSerializer


class CourseReadOnlySerializer(serializers.ModelSerializer):
    """
    Serializer to list and retrieve courses
    """

    students_count = serializers.ReadOnlyField(source='students.count')
    teams_count = serializers.ReadOnlyField(source='teams.count')
    team_in = serializers.SerializerMethodField()
    instructor = UserSerializer()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'duration',
            'form_method',
            'member_count_primary',
            'team_count_primary',
            'member_count_secondary',
            'team_count_secondary',
            'floating_band',
            'is_confirmed',
            'instructor',
            'students_count',
            'teams_count',
            'team_in',
            'formed_students_count',
        ]
        read_only_fields = ['is_confirmed']

    def get_team_in(self, course):
        try:
            team = Team.objects.get(course=course, members=self.context['request'].user)
            return TeamSerializer(team).data
        except Team.DoesNotExist:
            return None


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer to update one course
    """

    form_method = serializers.ChoiceField([1, 2, 3, 4, 5])

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'duration',
            'form_method',
            'member_count_primary',
            'team_count_primary',
            'member_count_secondary',
            'team_count_secondary',
            'floating_band',
        ]
        min_kwargs = {'min_value': 0}
        extra_kwargs = {
            'duration': {'read_only': False},
            'member_count_primary': min_kwargs,
            'member_count_secondary': min_kwargs,
            'team_count_primary': min_kwargs,
            'team_count_secondary': min_kwargs,
            'floating_band': min_kwargs,
        }

    def validate(self, data: dict):
        """
        Validate whether the member counts satisfy the limitation of number of students
        in the course
        """
        course = self.instance
        form_method = data.get('form_method') or course.form_method
        member_count_primary = data.get('member_count_primary') or course.member_count_primary
        member_count_secondary = data.get('member_count_secondary') or course.member_count_secondary
        team_count_primary = data.get('team_count_primary') or course.team_count_primary
        team_count_secondary = data.get('team_count_secondary') or course.team_count_secondary

        if (form_method == 4 or form_method == 5) and \
                (member_count_primary % 2 > 0 or member_count_secondary % 2 > 0):
            raise serializers.ValidationError('Member counts must be even numbers!')

        if member_count_primary * team_count_primary + \
                member_count_secondary * team_count_secondary != course.students.count():
            raise serializers.ValidationError('Invalid combination of member counts and team counts!')
        return data


class CourseCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create a new course
    """

    instructor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ['id', 'title', 'instructor']


class CourseRemoveStudentSerializer(serializers.Serializer):
    """
    Serializer to remove one student from a given course
    """

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_user(self, user):
        if not user.courses_in.filter(pk=self.context['course'].pk).exists():
            raise serializers.ValidationError('The student is not in this course!')
        return user
