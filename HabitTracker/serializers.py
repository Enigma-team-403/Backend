from rest_framework import serializers
from .models import Habit, DailyProgress

from rest_framework import serializers
from .models import Habit, DailyProgress

from rest_framework import serializers
from .models import Habit, DailyProgress

class HabitSerializer(serializers.ModelSerializer):
    daily_target = serializers.ReadOnlyField()

    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'duration', 'goal', 'progress', 'topic', 'section', 'daily_target']

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value

    def validate_goal(self, value):
        if value <= 0:
            raise serializers.ValidationError("Goal must be a positive number.")
        return value

class DailyProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProgress
        fields = ['id', 'habit', 'date', 'completed_amount']
class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'duration','goal', 'progress', 'topic', 'section']

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be a positive number.")
        return value







# from rest_framework import serializers
# from .models import Habit, DailyProgress

# class DailyProgressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DailyProgress
#         fields = ['id', 'habit', 'date', 'completed']

# class HabitSerializer(serializers.ModelSerializer):
#     daily_progress = DailyProgressSerializer(many=True, read_only=True)
#     class Meta:
#         model = Habit
#         fields = ['id', 'name', 'description', 'duration','goal', 'progress', 'topic', 'section', 'daily_progress']

#     def validate_duration(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Duration must be a positive number.")
#         return value

