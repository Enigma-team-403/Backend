from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from rest_framework.pagination import PageNumberPagination


from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

# Get the custom user model
User = get_user_model()

class ChatPagination(PageNumberPagination):
    page_size = 10

class ChatListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Fetch all chats of the authenticated user and show the users they started chats with."""
        # Get the chats the authenticated user is part of
        chats = Chat.objects.filter(participants=request.user)
        participants = []

        # Iterate over each chat and get the other participant(s)
        for chat in chats:
            # Exclude the authenticated user from the list of participants
            other_participant = chat.participants.exclude(user_id=request.user.user_id).first()  # Use user_id instead of id
            if other_participant:
                 participants.append({
                    "username": other_participant.username,
                    "user_id": other_participant.user_id,
                    "chat_id": chat.id  # Add chat_id
                })

        return Response({"chats": participants}, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new chat between the authenticated user and another user."""
        participant_username = request.data.get('participant')
        if not participant_username:
            return Response({"detail": "Participant is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the participant user
        try:
            participant = User.objects.get(username=participant_username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prevent creating duplicate chats
        existing_chat = Chat.objects.filter(participants=request.user).filter(participants=participant).first()
        if existing_chat:
            return Response({"detail": "Chat with this participant already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Restrict to exactly two participants
        chat = Chat.objects.create()
        chat.participants.add(request.user, participant)
        chat.save()

        serializer = ChatSerializer(chat)
        return Response({"message": "Chat created!", "chat": serializer.data}, status=status.HTTP_201_CREATED)


class ChatDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
        """Send a new message to a specific chat."""
        chat = get_object_or_404(Chat, pk=pk)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        if not content:
            return Response({"detail": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(chat=chat, sender=request.user, content=content)
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
        """Send a message to a specific chat."""
        chat = get_object_or_404(Chat, id=chat_id)

        if request.user not in chat.participants.all():
            return Response({"detail": "You are not a participant in this chat."}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        if not content:
            return Response({"detail": "Message content is required."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(chat=chat, sender=request.user, content=content)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

