from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommunityViewSet
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'communities', views.CommunityViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'user_habits', views.UserHabitViewSet, basename='user-habits')

urlpatterns = [
    path('', include(router.urls)),  
    path('api/community/communities/', views.community_list_view, name='community-list'),
]

