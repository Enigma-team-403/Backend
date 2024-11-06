from django.urls import path
from members.views import (
	UserRegistrationAPIView,
	UserLoginAPIView,
	UserViewAPI,
	UserLogoutViewAPI)
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
	path('user/register/', UserRegistrationAPIView.as_view()),
	path('user/login/', UserLoginAPIView.as_view()),
	path('user/', UserViewAPI.as_view()),
	path('user/logout/', UserLogoutViewAPI.as_view()),
    path('admin/', admin.site.urls),
    
    path('auth/', include('social_django.urls', namespace='social'))
]