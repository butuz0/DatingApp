from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


# Create your models here.
class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-updated']),
        ]
        ordering = ['-updated']

    def __iter__(self):
        messages = self.messages.all()
        for message in messages:
            yield message


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message_text = models.TextField()
    message_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]
        ordering = ['created_at']
