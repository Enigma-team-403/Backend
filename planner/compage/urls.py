from django.urls import path

from .views import AddMemberToCommunity


urlpatterns = [
    path('community/<int:community_id>/add_member/', AddMemberToCommunity.as_view(), name='add_member_to_community'),

]

