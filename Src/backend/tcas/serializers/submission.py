from rest_framework import serializers

from tcas.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
        fields = '__all__'
        extra_kwargs = {
            'percentage': {'min_value': 0, 'max_value': 100},
        }

    def validate(self, attrs: dict):
        course = attrs.get('course') or self.instance.course
        total = sum([(sub.percentage if sub != self.instance else 0) for sub in course.submissions.all()]) + attrs['percentage']
        if total > 100:
            raise serializers.ValidationError('The total percentage of the submissions of one course cannot exceed 100!')
        return attrs
