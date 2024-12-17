from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'communities', views.CommunityViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'user_habits', views.UserHabitViewSet, basename='user-habits')

urlpatterns = [
    path('', include(router.urls)),  # Automatically include all routes from the router
=======
from .views import CommunityViewSet,SearchCommunityView,UserMembershipRequestsView,MembershipRequestViewSet,send_membership_request ,view_membership_requests,manage_membership_request #,SendMembershipRequestByNameView
from . import views


router = DefaultRouter()
router.register(r'communities', CommunityViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'user_habits', views.UserHabitViewSet, basename='user-habits')
router.register(r'membership_requests', MembershipRequestViewSet) # اضافه کردن MembershipRequestViewSet

urlpatterns = [
    path('', include(router.urls)),  
    path('search/', SearchCommunityView.as_view(), name='search_community'),
    path('membership_requests_old/', UserMembershipRequestsView.as_view(), name='user-membership-requests'),
    path('send_membership_request/', send_membership_request, name='send-membership-request'),
    path('communities/<int:community_id>/view_membership_requests/', view_membership_requests, name='view-membership-requests'), 
    path('communities/<int:community_id>/manage_membership_request/', manage_membership_request, name='manage-membership-request'), 
>>>>>>> backendWithoutToken
]

