from django.contrib import admin
from django.urls import path, include
# Ensure that consumers is imported from the correct app directory





urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path('api/', include('planner.urls')),
    path('api/', include('HabitTracker.urls')),
    path('', include('planner.urls')),
    path('', include('HabitTracker.urls')),
    
    path("chat/", include("chat.urls")),
]