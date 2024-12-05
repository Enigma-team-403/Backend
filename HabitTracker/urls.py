from django.urls import path
from . import views

urlpatterns = [
    path('habits/', views.habits_list_view, name='habits-list'),
    path('habits/create/', views.habit_create_view, name='habit-create'),
    path('habits/<int:pk>/reset/', views.habit_reset_view, name='habit-reset'),
    path('habits/<int:pk>/delete/', views.habit_delete_view, name='habit-delete'),
    path('habits/<int:habit_id>/edit/', views.habit_edit_view, name='habit-edit'),  # Add edit URL pattern
    path('habit/<int:habit_id>/', views.habit_detail, name='habit-detail'),
]
