from django.contrib import admin
from django.urls import path, include

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('api/', include('boards.urls')),
    
    # path('api/', include('cards.urls')),
    # path('api/', include('boards.urls.boards_urls')),
    # path('api/', include('boards.urls.labels_urls')),
    # path('api/', include('boards.urls.lists_urls')),
    ]
