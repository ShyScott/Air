from rest_framework import serializers

from tcas.models import Course, User, Team
from .team import TeamSerializer


class CourseListSerializer(serializers.ModelSerializer):
    """
    Serializer to list the courses
    """

    students_count = serializers.ReadOnlyField(source='students.count')
    team_in = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'duration', 'students_count', 'team_in']

    def get_team_in(self, obj):
        try:
            team = Team.objects.get(course=obj, members=self.context['request'].user)
            return TeamSerializer(team).data
        except Team.DoesNotExist:
            return None


class CourseSerializer(CourseListSerializer):
    """
    Serializer to retrieve, create, update and delete one course (with verbose information)
    """

    form_method = serializers.ChoiceField([1, 2, 3, 4, 5], required=False)
    member_count_primary = serializers.IntegerField(min_value=0, required=False)
    team_count_primary = serializers.IntegerField(min_value=0, required=False)
    member_count_secondary = serializers.IntegerField(min_value=0, required=False)
    team_count_secondary = serializers.IntegerField(min_value=0, required=False)
    floating_band = serializers.FloatField(min_value=0, required=False)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'duration',
            'students_count',
            'form_method',
            'member_count_primary',
            'team_count_primary',
            'member_count_secondary',
            'team_count_secondary',
            'floating_band',
        ]

    def validate(self, data):
        """
        Validate whether the member counts satisfy the limitation of number of students
        in the course
        """
        if self.instance is None:
            return data
        if data['member_count_primary'] * data['team_count_primary'] + \
                data['member_count_secondary'] * data['team_count_secondary'] != self.instance.students.count():
            raise serializers.ValidationError('Invalid combination of member counts and team counts!')
        return data

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)


class CourseRemoveStudentSerializer(serializers.Serializer):
    """
    Serializer to remove one student from a given course
    """

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate_user(self, user):
        if not user.courses_in.filter(pk=self.context['course'].pk).exists():
            raise serializers.ValidationError('The student is not in this course!')
        return user
