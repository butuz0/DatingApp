from django.urls import path
from . import views

app_name = 'statistic'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile_likes/', views.profile_likes, name='profile_likes'),
    path('profile_likes_data/<int:days>/', views.get_profile_likes_data, name='profile_likes_data'),
    path('relationship_types/', views.relationship_types_analysis, name='relationship_types_analysis'),
    path('age_groups/', views.age_analysis, name='age_analysis'),
    path('profile_visits/', views.profile_visits, name='profile_visits'),
    path('profile_visits_data/<int:days>/', views.get_profile_visits_data, name='profile_visits_data'),
    path('monthly_likes/', views.monthly_likes, name='monthly_likes'),
    path('interests_groups_data/', views.interests_groups_analysis, name='interests_groups_data'),
    path('most_popular_interests_data/<int:amount>/', views.most_popular_interests_analysis,
         name='most_popular_interests_data'),
    path('interests/', views.interests_page, name='interests_analysis'),
]
