from django.db import models
from django.conf import settings
import random
from django.contrib.auth.models import User

def unique_generator(length=10):
    source = "abcdefghijklmnopqrstuvwxyz"
    return ''.join(random.choice(source) for _ in range(length))


# GroupChat Model
class GroupChat(models.Model):
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="created_chats"
    )
    title = models.CharField(max_length=50)
    unique_code = models.CharField(max_length=10, default=unique_generator)
    date_created = models.DateTimeField(auto_now_add=True)


# Member Model
class Member(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="group_memberships"
    )  # Fixed: Only one user field
    chat = models.ForeignKey(
        GroupChat, 
        on_delete=models.CASCADE, 
        related_name="members"
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# Message Model
class Message(models.Model):
    chat = models.ForeignKey(
        GroupChat, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="authored_messages"
    )
    text = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)


# VideoThread Model
class VideoThread(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
