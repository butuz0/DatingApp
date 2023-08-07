from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('list/', views.list_people, name='list_people'),
    path('<username>', views.user_detail, name='user_detail'),
    path('like/', views.like_user, name='like_user'),
]
