from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet
from . import views
from .views import UserHabitViewSet


router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
router.register(r'user-habits', UserHabitViewSet, basename='user-habits')

urlpatterns = [
    path('', include(router.urls)),
    path('habits/', views.habits_list_view, name='habits-list'),
    path('habits/create/', views.habit_create_view, name='habit-create'),
    path('habits/<int:pk>/reset/', views.habit_reset_view, name='habit-reset'),
    path('habits/<int:pk>/delete/', views.habit_delete_view, name='habit-delete'),
    path('habits/<int:habit_id>/edit/', views.habit_edit_view, name='habit-edit'),  # Add edit URL pattern
    path('habit/<int:habit_id>/', views.habit_detail, name='habit-detail'),
]

