# chat_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Chat, Message
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.chat_id = self.scope['url_route']['kwargs']['chat_id']
            self.chat_group_name = f'chat_{self.chat_id}'

            # Fetch the chat to ensure it exists
            chat = await self.get_chat(self.chat_id)

            # Join room group
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"WebSocket connected: {self.chat_group_name}")
        except Exception as e:
            logger.error(f"Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: {self.chat_group_name}")

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            sender_username = text_data_json.get('sender_username')

            if not message or not sender_username:
                raise ValueError("Missing 'message' or 'sender_username' in payload")

            # Fetch sender and chat
            sender = await self.get_user_by_username(sender_username)
            chat = await self.get_chat(self.chat_id)

            # Save message to database
            message_obj = await self.save_message(chat, sender, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                    'timestamp': str(message_obj.timestamp)
                }
            )
        except Exception as e:
            logger.error(f"Error in receive: {e}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))
            await self.close()

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))

    # Helper methods
    async def get_user_by_username(self, username):
        try:
            return await User.objects.aget(username=username)
        except User.DoesNotExist:
            raise ValueError(f"User with username {username} does not exist")

    async def get_chat(self, chat_id):
        try:
            return await Chat.objects.aget(id=chat_id)
        except Chat.DoesNotExist:
            raise ValueError(f"Chat with ID {chat_id} does not exist")

    async def save_message(self, chat, sender, content):
        return await Message.objects.acreate(chat=chat, sender=sender, content=content)