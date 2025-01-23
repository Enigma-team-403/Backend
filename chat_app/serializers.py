from rest_framework import serializers
from .models import Message, Chat

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    timestamp = serializers.DateTimeField(format='%m/%d/%Y %I:%M %p')

    class Meta:
        model = Message
        fields = ['chat_id','id','sender', 'content', 'timestamp', 'chat']

class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.StringRelatedField(many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at']
