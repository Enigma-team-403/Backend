
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.pagination import PageNumberPagination
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Get the custom user model
User = get_user_model()

class ChatPagination(PageNumberPagination):
    page_size = 10


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()

class ChatListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Create a new chat with multiple participants."""
        participant_usernames = request.data.get('participants', [])
        if not participant_usernames:
            return Response({"detail": "At least one participant is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the participant users
        participants = []
        for username in participant_usernames:
            try:
                user = User.objects.get(username=username)
                participants.append(user)
            except User.DoesNotExist:
                return Response({"detail": f"User with username {username} not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prevent creating duplicate chats with the same participants
        existing_chat = Chat.objects.filter(participants=request.user)
        for participant in participants:
            existing_chat = existing_chat.filter(participants=participant)
        if existing_chat.exists():
            return Response({"detail": "Chat with these participants already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the chat and add participants
        chat = Chat.objects.create()
        chat.participants.add(request.user)
        for participant in participants:
            chat.participants.add(participant)
        chat.save()

        serializer = ChatSerializer(chat)
        return Response({"message": "Chat created!", "chat": serializer.data}, status=status.HTTP_201_CREATED)
class ChatDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, chat_id, message_id):
        """Delete a specific message."""
        chat = get_object_or_404(Chat, id=chat_id)

        # Ensure the user is a participant in the chat
        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        # Fetch the message
        message = get_object_or_404(Message, id=message_id, chat=chat)

        # Ensure the user is the sender of the message
        if message.sender != request.user:
            return Response({"detail": "You can only delete your own messages."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the message
        message.delete()
        return Response({"detail": "Message deleted."}, status=status.HTTP_204_NO_CONTENT)
    def get(self, request, pk):
        """Fetch details of a specific chat with paginated messages."""
        chat = get_object_or_404(Chat, pk=pk)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        paginator = ChatPagination()
        messages = chat.messages.all()
        paginated_messages = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(paginated_messages, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, pk):
        """Send a new message to a specific chat and broadcast it to all participants."""
        chat = get_object_or_404(Chat, pk=pk)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        if not content:
            return Response({"detail": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the message
        message = Message.objects.create(chat=chat, sender=request.user, content=content)

        # Broadcast the message to the chat group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat.id}',  # Group name
            {
                'type': 'chat_message',  # Event type
                'message': message.content,
                'sender': message.sender.username,
                'timestamp': str(message.timestamp)
            }
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id, message_id):
        """Fetch details of a specific message."""
        chat = get_object_or_404(Chat, id=chat_id)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        message = get_object_or_404(Message, id=message_id, chat=chat)

        return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)

    def delete(self, request, chat_id, message_id):
        """Delete a specific message."""
        chat = get_object_or_404(Chat, id=chat_id)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        message = get_object_or_404(Message, id=message_id, chat=chat)

        if message.sender != request.user:
            return Response({"detail": "You can only delete your own messages."}, status=status.HTTP_403_FORBIDDEN)

        message.delete()
        return Response({"detail": "Message deleted."}, status=status.HTTP_204_NO_CONTENT)


class MessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, chat_id):
        """Fetch all messages from a specific chat without pagination."""
        chat = get_object_or_404(Chat, id=chat_id)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        messages = chat.messages.all()  # Retrieve all messages without pagination
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, chat_id):
        """Send a message to a specific chat and broadcast it to all participants."""
        chat = get_object_or_404(Chat, id=chat_id)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        if not content:
            return Response({"detail": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the message
        message = Message.objects.create(chat=chat, sender=request.user, content=content)

        # Broadcast the message to the chat group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{chat.id}',  # Group name
            {
                'type': 'chat_message',  # Event type
                'message': message.content,
                'sender': message.sender.username,
                'timestamp': str(message.timestamp)
            }
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)