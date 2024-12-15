from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RegisterUserView
from .views import CommunityListView, RegisterUserView
from .views import CreateCommunityView, CommunityListView
from .views import UpdateCommunityView
from .views import DeleteCommunityView,CommunityDetailView



# Create a router and register viewsets
router = DefaultRouter()
router.register(r'communities', views.CommunityViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'user_habits', views.UserHabitViewSet, basename='user-habits')

urlpatterns = [
    path('', include(router.urls)),  # Automatically include all routes from the router
    path('communities/<int:pk>/user-progress/', views.CommunityViewSet.as_view({'get': 'user_progress'}), name='user-progress'),
    path('community/<int:community_id>/register/', RegisterUserView.as_view(), name='register-user'),
    path('communities/', CommunityListView.as_view(), name='community-list'),
    path('community/<int:community_id>/register/', RegisterUserView.as_view(), name='register-user'),
    path('communities/', CommunityListView.as_view(), name='community-list'),
    path('community/create/', CreateCommunityView.as_view(), name='create-community'),
    path('community/<int:community_id>/edit/', UpdateCommunityView.as_view(), name='edit-community'),
    path('community/<int:community_id>/delete/', DeleteCommunityView.as_view(), name='delete-community'),
    path('community/<int:community_id>/', CommunityDetailView.as_view(), name='community-detail'),
]

