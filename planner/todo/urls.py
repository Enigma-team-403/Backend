from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TagViewSet, ListViewSet, SubTaskViewSet, CommentViewSet, TaskTagViewSet

router = DefaultRouter()
router.register(r'lists', ListViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubTaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'tasktags', TaskTagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/filter_by_tag/', TaskViewSet.as_view({'get': 'filter_by_tag'}), name='task-filter-by-tag'),
    path('tags/list_tags/', TagViewSet.as_view({'get': 'list_tags'}), name='list-tags'),
    path('tasks/search/', TaskViewSet.as_view({'get': 'search'}), name='task-search'),
    path('tasks/filter_by_month/', TaskViewSet.as_view({'get': 'filter_by_month'}), name='task-filter-by-month'),
]
