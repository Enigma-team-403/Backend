from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import CommunityViewSet,SearchCommunityView,UserMembershipRequestsView,MembershipRequestViewSet,send_membership_request ,view_membership_requests,manage_membership_request,community_list_view,UpdateCommunityHabitProgressView ,update_community_habit_progress
from . import views


router = DefaultRouter()
router.register(r'communities', CommunityViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'user_habits', views.UserHabitViewSet, basename='user-habits')
router.register(r'membership_requests', MembershipRequestViewSet) # اضافه کردن MembershipRequestViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  
    path('search/', SearchCommunityView.as_view(), name='search_community'),
    path('membership_requests_old/', UserMembershipRequestsView.as_view(), name='user-membership-requests'),
    path('send_membership_request/', send_membership_request, name='send-membership-request'),
    path('communities/<int:community_id>/view_membership_requests/', view_membership_requests, name='view-membership-requests'), 
    path('communities/<int:community_id>/manage_membership_request/', manage_membership_request, name='manage-membership-request'), 
    path('communities/<int:pk>/accept_membership_request/', CommunityViewSet.as_view({'post': 'accept_membership_request'}), name='community-accept-membership-request'),
    path('community-list/', community_list_view, name='community-list'),

    path('communities/<int:pk>/linked_habits/', CommunityViewSet.as_view({'get': 'linked_habits', 'post': 'linked_habits'}), name='community-linked-habits'),
    path('communities/<int:pk>/add_habits/', CommunityViewSet.as_view({'post': 'add_habits'}), name='community-add-habits'),
    path('communities/<int:pk>/details/', CommunityViewSet.as_view({'get': 'details', 'put': 'details'}), name='community-details'),
    path('communities/<int:pk>/add_members/', CommunityViewSet.as_view({'get': 'add_members', 'post': 'add_members'}), name='community-add-members'),
    path('communities/<int:pk>/membership_requests/', CommunityViewSet.as_view({'get': 'membership_requests'}), name='community-membership-requests'),
    path('communities/<int:pk>/edit/', CommunityViewSet.as_view({'put': 'update'}), name='community-update'),  # ویرایش یک کامیونیتی
    path('communities/<int:pk>/delete/', CommunityViewSet.as_view({'delete': 'destroy'}), name='community-delete'),  # حذف یک کامیونیتی
    path('communities/<int:pk>/', CommunityViewSet.as_view({'get': 'retrieve'}), name='community-retrieve'),  # دریافت جزئیات یک کامیونیتی),

    path('communities/<int:pk>/members/', CommunityViewSet.as_view({'get': 'members'}), name='community-members'),  # مسیر مورد نظر    
    path('communities/my_communities/', CommunityViewSet.as_view({'get': 'my_communities'}), name='my-communities'), 
    path('communities/joined_communities/', CommunityViewSet.as_view({'get': 'joined_communities'}), name='joined-communities'),
    # path('communities/<int:community_id>/update_habit_progress/', update_community_habit_progress, name='update-community-habit-progress'),
    path('recommended_communities/', CommunityViewSet.as_view({'get': 'recommended_communities'}), name='recommended-communities'),
    path('communities/<int:community_id>/update_habit_progress/', UpdateCommunityHabitProgressView.as_view(), name='update-community-habit-progress'),]