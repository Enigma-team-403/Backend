

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards.views import BoardViewSet,ListViewSet,LabelViewSet

router1 = DefaultRouter()
router1.register(r'boards', BoardViewSet, basename='boards')
router1.register(r'lists', ListViewSet, basename='lists')
router1.register(r'labels', LabelViewSet, basename='labels')





urlpatterns = [
    path('', include(router1.urls))
]