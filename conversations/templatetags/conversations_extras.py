from django import template
from django.db.models import Q
from conversations.models import Message

register = template.Library()


@register.filter
def unread_messages_count(conversation, user):
    return (Message.objects
            .filter(conversation=conversation, message_read=False)
            .filter(~Q(created_by=user)).count())
