from django.urls import path
from . import views

app_name = 'statistic'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile_likes/', views.profile_likes, name='profile_likes'),
    path('profile_likes_data/<int:days>/', views.get_profile_likes_data, name='profile_likes_data'),
    path('relationship_types/', views.relationship_types_analysis, name='users_analysis'),
    path('age_groups/', views.age_analysis, name='users_analysis2')
]
