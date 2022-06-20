from rest_framework import serializers

from .models import Jobs, Steps

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = [
            'step',
            'status', 
            'start_time', 
            'end_time',
        ]
