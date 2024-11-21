

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards.views import BoardViewSet,ListViewSet,LabelViewSet

router1 = DefaultRouter()
router1.register(r'boards', BoardViewSet, basename='boards')


router2 = DefaultRouter()
router2.register(r'lists', ListViewSet, basename='lists')


router3 = DefaultRouter()
router3.register(r'labels', LabelViewSet, basename='labels')



# urlpatterns = [
#     path('', include(router1.urls)),
#     path('', include(router2.urls)),
#     path('', include(router3.urls)),

# ]

urlpatterns = router1.urls + router2.urls + router3.urls