from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

from . import views

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),  # This will handle all the routes for your ProfileViewSet
    path('user/<str:username>/', views.UserDetailView.as_view(), name='user-detail'),
]
