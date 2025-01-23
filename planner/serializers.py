from rest_framework import serializers
from .models import Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'start_time', 'end_time', 'completed']

    def validate_priority(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Priority must be between 1 and 5.")
        return value

