from rest_framework import serializers

from tcas.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    percentage = serializers.IntegerField(min_value=0, max_value=100)

    class Meta:
        model = Submission
        fields = '__all__'

    def validate(self, attrs):
        total = sum([sub.percentage for sub in attrs['course'].submissions.all()]) + attrs['percentage']
        if total > 100:
            raise serializers.ValidationError('The total percentage of the submissions of one course cannot exceed 100!')
        return attrs
