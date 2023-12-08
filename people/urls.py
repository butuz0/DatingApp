from django.urls import path
from . import views
from blog import views as blog_views

app_name = 'people'

urlpatterns = [
    path('', views.list_people, name='list_people'),
    path('<username>', views.user_detail, name='user_detail'),
    path('activity/', views.user_activity, name='user_activity'),
    path('like/', views.like_user, name='like_user'),
    path('<username>/new_post/', blog_views.create_post, name='create_post'),
]
