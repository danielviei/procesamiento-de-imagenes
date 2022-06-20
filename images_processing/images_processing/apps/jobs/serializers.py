from rest_framework import serializers

from .models import Jobs, Steps

class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Steps
        fields = [
            'step',
            'status', 
            'start_time', 
            'end_time',
        ]

class JobSerializer(serializers.ModelSerializer):
    steps = StepsSerializer(many=True, read_only=True)
    class Meta:
        model = Jobs
        fields = [
            'id',
            'step',
            'steps',
            'status',
        ]
