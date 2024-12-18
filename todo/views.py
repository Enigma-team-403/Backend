from rest_framework import status, viewsets,permissions
from .models import Task, SubTask, Comment ,List ,Tag, TaskTag
from .serializers import TaskSerializer, SubTaskSerializer, CommentSerializer ,ListSerializer ,TaskTagSerializer, TagSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.dateparse import parse_date

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def filter_by_tag(self, request):
        tag_name = request.query_params.get('tag', None)
        if tag_name:
            tasks = self.queryset.filter(tag__name=tag_name)
        else:
            tasks = self.queryset.none()

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])    
    def filter_by_month(self, request):
        date_str = request.query_params.get('month', None)
        if date_str:
            date = parse_date(date_str)
            if date:
                tasks = self.queryset.filter(create_time__year=date.year, create_time__month=date.month)
            else:
                tasks = self.queryset.none()
        else:
            tasks = self.queryset.none()

        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])    
    def search(self, request):
        query = request.query_params.get('task', None)
        if query:
            tasks = self.queryset.filter(title__icontains=query)
            results = [{'task': task.title, 'list': task.list.title} for task in tasks]
        else:
            results = []

        return Response(results)



class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('subtask', None)
        if query:
            tasks = self.queryset.filter(title__icontains=query)
            results = [{'task': task.title, 'list': task.list.title} for task in tasks]
        else:
            results = []

        return Response(results)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        comment_data = request.data
        comment_data['task'] = task.id
        comment_serializer = CommentSerializer(data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='list-tags')    
    def list_tags(self, request):
        tags = self.queryset.all()
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)


class TaskTagViewSet(viewsets.ModelViewSet):
    queryset = TaskTag.objects.all()
    serializer_class = TaskTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
