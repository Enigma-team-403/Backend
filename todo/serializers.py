from rest_framework import serializers
from .models import Task, SubTask , Comment ,Tag, TaskTag, List
from django.contrib.auth.models import User # افزودن مدل User
from django.contrib.auth import get_user_model

User = get_user_model()


class SubTaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    list = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SubTask
        fields = '__all__'

    def get_list(self, obj):
        return obj.task.list.id

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TaskTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTag
        fields = '__all__'



class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(source='task_tags.tag', many=True, read_only=True)
    list = serializers.PrimaryKeyRelatedField(queryset=List.objects.all())
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        for subtask_data in subtasks_data:
            SubTask.objects.create(task=task, **subtask_data)
        for tag_data in tags_data:
            tag = Tag.objects.get(id=tag_data['id'])
            TaskTag.objects.create(task=task, tag=tag)
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.note = validated_data.get('note', instance.Note)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.start_task = validated_data.get('start_task', instance.start_task)
        instance.end_task = validated_data.get('end_task', instance.end_task)
        instance.save()

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get('id')
            if subtask_id:
                subtask = SubTask.objects.get(id=subtask_id, task=instance)
                subtask.title = subtask_data.get('title', subtask.title)
                subtask.description = subtask_data.get('description', subtask.description)
                subtask.completed = subtask_data.get('completed', subtask.completed)
                subtask.priority = subtask_data.get('priority', subtask.priority)
                subtask.save()
            else:
                SubTask.objects.create(task=instance, **subtask_data)

        for tag_data in tags_data:
            tag = Tag.objects.get(id=tag_data['id'])
            TaskTag.objects.create(task=instance, tag=tag)

        return instance


class ListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = List
        fields = '__all__'
