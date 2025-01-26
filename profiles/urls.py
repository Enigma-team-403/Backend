# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ProfileViewSet
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# router = DefaultRouter()
# router.register(r'profiles', ProfileViewSet, basename='profile')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('profiles/my_profile/', ProfileViewSet.as_view({'get': 'my_profile'}), name='my-profile'),
#     path('profiles/edit_profile/', ProfileViewSet.as_view({'put': 'edit_profile'}), name='edit-profile'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('profiles/my_profile/', ProfileViewSet.as_view({'get': 'my_profile'}), name='my-profile'),
    path('profiles/edit_profile/', ProfileViewSet.as_view({'put': 'edit_profile'}), name='edit-profile'),
]

