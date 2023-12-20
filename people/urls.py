from django.urls import path
from . import views
from blog import views as blog_views

app_name = 'people'

urlpatterns = [
    path('', views.list_people, name='list_people'),
    path('<username>', views.user_detail, name='user_detail'),
    path('activity/', views.user_activity, name='user_activity'),
    path('like/', views.like_user, name='like_user'),
    path('findme/', views.find_best_match, name='findme'),
    path('report/<reported_user_id>', views.report_user, name='report_user'),
]
