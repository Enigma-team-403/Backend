from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path('api/', include('planner.urls')),
    path('api/', include('HabitTracker.urls')),
    path('', include('planner.urls')),
    path('', include('HabitTracker.urls')),
    
    # cd planner and .venv\scripts\activate and runserver To run the following lines
    
    path('admin/', admin.site.urls),
    path('api/todo/', include('todo.urls')),
    path('api/profiles/', include('profiles.urls')), 
    path('api/community/', include('community.urls')),
    path('api/Habits/', include('HabitTracker.urls')),
    path('api/interest/', include('interest.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    ]
