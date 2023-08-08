from django.contrib import admin
from .models import Conversation, Message


# Register your models here.
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'updated']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'created_by', 'created_at']
