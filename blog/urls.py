from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('new_post/', views.create_post, name='create_post'),
    path('edit_blog/', views.edit_blog, name='edit_blog'),
    path('get_post/<post_id>', views.get_post, name='get_post'),
    path('edit_post/<post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<post_id>', views.delete_post, name='delete_post'),
    path('add_comment/<post_id>', views.add_comment, name='add_comment'),
    path('delete_comment/<post_id>/<comment_id>', views.delete_comment, name='delete_comment'),
    path('like_comment/', views.like_comment, name='like_comment'),
    path('like_post/', views.like_post, name='like_post'),
]
