from django.contrib import admin
from chat.models import Member, GroupChat, Message

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'unique_code', 'date_created')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'date_created')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'author', 'text', 'date_created')
