# from django.urls import path,include
# from rest_framework_simplejwt import views as jwt_views
# from members.views import (
# 	UserRegistrationAPIView,
# 	UserLoginAPIView,
# 	UserViewAPI,
# 	UserLogoutViewAPI, MemberViewSet)
# from django.contrib import admin
# from rest_framework import routers


# router = routers.DefaultRouter()
# router.register(r'lists', MemberViewSet, basename='member')

# urlpatterns = [
# 	path('user/register/', UserRegistrationAPIView.as_view()),
# 	path('user/login/', UserLoginAPIView.as_view()),
# 	path('user/', UserViewAPI.as_view()),
# 	path('user/logout/', UserLogoutViewAPI.as_view()),
#     path('admin/', admin.site.urls),
#     path('token/', jwt_views.TokenObtainPairView.as_view(),name = 'token_obtain_pair'),
#     path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name = 'token_refresh'),
#     path('', include(router.urls))
# ]
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from members.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserViewAPI,
	UserLogoutViewAPI, MemberViewSet)
from django.contrib import admin
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'lists', MemberViewSet, basename='member')

urlpatterns = [
	path('user/register/', UserRegistrationAPIView.as_view()),
	path('user/login/', UserLoginAPIView.as_view()),
	path('user/', UserViewAPI.as_view()),
	path('user/logout/', UserLogoutViewAPI.as_view()),
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(),name = 'token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name = 'token_refresh'),
    path('', include(router.urls))
]
