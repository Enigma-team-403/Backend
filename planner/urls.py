from django.urls import path , include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TaskViewSet, filter_tasks, update_task_status, get_task_status, planner_view



router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),

    path('tasks/filter/', filter_tasks, name='filter_tasks'),
    path('tasks/<int:task_id>/update-status/', update_task_status, name='update_task_status'),
    path('tasks/<int:task_id>/status/', get_task_status, name='get_task_status'),
    path('planner/', views.planner_view, name='planner'),
    path('planner/form/', views.planner_form_view, name='planner-form'),
    path('add/', views.add_task, name='add_task'),
    path('toggle-completed/<int:task_id>/', views.toggle_completed, name='toggle_completed'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),  
    path('task/change-priority/<int:task_id>/<int:priority>/', views.change_priority, name='change_priority'),
    path('checklist/toggle_completed/<int:item_id>/', views.toggle_checklist_item_completed, name='toggle_checklist_item_completed'),
    path('checklist/delete/<int:item_id>/', views.delete_checklist_item, name='delete_checklist_item'),
    ]

