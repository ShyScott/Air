from rest_framework import serializers

from tcas.models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    percentage = serializers.IntegerField(min_value=0, max_value=100)

    class Meta:
        model = Submission
        fields = '__all__'
