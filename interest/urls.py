from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterestViewSet, UserInterestViewSet
from . import views

router = DefaultRouter()
router.register(r'interests', InterestViewSet)
router.register(r'user_interests', UserInterestViewSet, basename='user_interests')

urlpatterns = [
    path('', include(router.urls)),
    path('select_interests/', views.select_interests, name='select-interests'),
    path('user_interests/save/', UserInterestViewSet.as_view({'post': 'save_user_interests'}), name='save-user-interests'),
]
