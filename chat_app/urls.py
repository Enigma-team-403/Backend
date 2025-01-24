from django.urls import path
from .views import ChatListCreateView, ChatDetailView, MessageListCreateView, MessageDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('chats/', ChatListCreateView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('messages/<int:chat_id>/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:chat_id>/detail/<int:message_id>/', MessageDetailView.as_view(), name='message-detail'),
]
