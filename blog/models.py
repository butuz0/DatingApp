from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    text = models.TextField(validators=[MaxLengthValidator(220)])
    image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']), ]

    def __str__(self):
        return f'{self.author.username} : {self.text[:10]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(validators=[MaxLengthValidator(120)])
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_created')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created']), ]

    def __str__(self):
        return f'{self.author.username} : {self.text[:10]}'
