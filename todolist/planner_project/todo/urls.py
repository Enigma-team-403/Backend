from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
    path('add/', views.add_task, name='add_task'),
    path('toggle-completed/<int:task_id>/', views.toggle_completed, name='toggle_completed'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),  
    path('task/change-priority/<int:task_id>/<int:priority>/', views.change_priority, name='change_priority')]

