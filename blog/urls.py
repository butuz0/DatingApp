from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('new_post/', views.create_post, name='create_post'),
    path('edit_blog/', views.edit_blog, name='edit_blog'),
    path('delete_post/<post_id>', views.delete_post, name='delete_post'),
]
