from rest_framework import serializers
from .models import Community, Category, Habit
from HabitTracker.models import Habit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description']


class CommunitySerializer(serializers.ModelSerializer):
    external_habits = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), many=True)

    class Meta:
        model = Community
        fields = '__all__'  
    def validate_category_ids(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("You can select a maximum of 2 categories.")
        return value

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        habits_data = validated_data.pop('habits')
        community = Community.objects.create(**validated_data)
        community.categories.set(categories_data)
        community.habits.set(habits_data)
        return community

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories')
        habits_data = validated_data.pop('habits')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        instance.categories.set(categories_data)
        instance.habits.set(habits_data)
        return instance
    
