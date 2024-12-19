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
    path('tasks/filter_by_month/', TaskViewSet.as_view({'get': 'filter_by_month'}), name='task-filter-by-month'),
    path('lists/filter_by_tag/', ListViewSet.as_view({'get': 'filter_by_tag'}), name='list-filter-by-tag'), 
    path('lists/filter_by_month/', ListViewSet.as_view({'get': 'filter_by_month'}), name='list-filter-by-month'),
    path('tags/list_tags/', TagViewSet.as_view({'get': 'list_tags'}), name='list-tags'),
    path('tasks/search/', TaskViewSet.as_view({'get': 'search'}), name='task-search'),
    path('subtasks/search/', SubTaskViewSet.as_view({'get': 'search'}), name='subtask-search'),    
    path('lists/search/', ListViewSet.as_view({'get': 'search'}), name='list-search'),
    path('tasks/<int:pk>/edit/', TaskViewSet.as_view({'put': 'edit'}), name='task-edit'),
    path('subtasks/<int:pk>/edit/', SubTaskViewSet.as_view({'put': 'edit'}), name='subtask-edit'),
    path('lists/<int:pk>/edit/', ListViewSet.as_view({'put': 'edit'}), name='list-edit'),
]
