from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Post


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']
