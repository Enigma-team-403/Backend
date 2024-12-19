from django.contrib import admin
from django.urls import path, include
# Ensure that consumers is imported from the correct app directory
from chat import views as chat_views


from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views
from chat import views as chat_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path('api/', include('planner.urls')),
    path('api/', include('HabitTracker.urls')),
    path('', include('planner.urls')),
    path('', include('HabitTracker.urls')),
    



    path('admin/', admin.site.urls),
    path('echo/', include('echo.urls')),
    path('chat/', include('chat.urls')),

  
]