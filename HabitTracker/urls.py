from . import views
from django.urls import path, include
from .views import HabitListView,HabitDeleteView,HabitUpdateView,UpdateProgressView  

urlpatterns = [
    path('habits/', HabitListView.as_view(), name='habits-list'),
    path('habits/create/', views.HabitCreateView.as_view(), name='habit-create'),
    path('habits/<int:pk>/delete/', HabitDeleteView.as_view(), name='habit-delete'),
    path('habits/<int:pk>/edit/', HabitUpdateView.as_view(), name='habit-edit'),  # مسیر برای ویرایش عادت    path('habit/<int:habit_id>/', views.habit_detail, name='habit-detail'),
    path('update-progress/', UpdateProgressView.as_view(), name='update-progress'),
    ]
