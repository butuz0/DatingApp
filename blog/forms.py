from django import forms
from django.forms import ModelForm
from .models import Post, Comment


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']


class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add new comment',
                                          'rows': '1'})
        }
