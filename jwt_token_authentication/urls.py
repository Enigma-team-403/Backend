from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path('api/', include('planner.urls')),
    path('api/', include('HabitTracker.urls')),
    path('', include('planner.urls')),
    path('', include('HabitTracker.urls')),
 
    ]
