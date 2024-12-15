# from rest_framework import serializers
# from .models import Community, Category, Habit
# from django import forms
# from .models import Community

# # serializers.py
# from rest_framework import serializers
# from .models import Community, Category, Habit

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name']  # Ensure you include fields you need


# class HabitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Habit
#         fields = ['id', 'name', 'description', 'user']  # Add any other relevant fields for Habit



# class CommunitySerializer(serializers.ModelSerializer):
#     # Linking category and habit using PrimaryKeyRelatedField
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     habit = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), required=True)

#     # Custom validation for category field
#     def validate_category(self, value):
#         # Ensure category is not empty
#         if not value:
#             raise serializers.ValidationError("Category is required.")
#         return value

#     # Create method to handle the creation of a community and its relationships
#     def create(self, validated_data):
#         category_data = validated_data.pop('category')
#         habit_data = validated_data.pop('habit')
        
#         # Ensure only one habit is assigned
#         community = Community.objects.create(**validated_data)
#         community.category = category_data
#         community.habit = habit_data
#         community.save()
#         return community

#     # Update method to handle updating a community and its relationships
#     def update(self, instance, validated_data):
#         category_data = validated_data.pop('category', None)
#         habit_data = validated_data.pop('habit', None)
        
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
        
#         if category_data:
#             instance.category = category_data
        
#         if habit_data:
#             instance.habit = habit_data
        
#         instance.save()
#         return instance

#     class Meta:
#         model = Community
#         fields = ['id', 'name', 'description', 'category', 'habit']  # Notice 'habit' is now singular






# class CommunityForm(forms.ModelForm):
#     class Meta:
#         model = Community
#         fields = ['name', 'description', 'category', 'habit']  # Ensure these match the model fields
from rest_framework import serializers
from .models import Community, Category, Habit
from django import forms
from .models import Community, Category, Habit
from django.contrib import admin
from .models import Community, Category, Habit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'description', 'category']

class CommunitySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    habit = HabitSerializer()

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'category', 'habit', 'owner']



class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description', 'category', 'habit']

    category = forms.ModelChoiceField(queryset=Category.objects.all())
    habit = forms.ModelChoiceField(queryset=Habit.objects.all())




@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'habit', 'owner']
    search_fields = ['name', 'category__name', 'habit__name']
