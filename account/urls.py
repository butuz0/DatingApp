from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.user_registration, name='user_register'),
    path('profile_register/', views.profile_registration, name='profile_register'),
    path('relationship/', views.relationship_type_form, name='relationship_form'),
    path('interests/', views.interests_form, name='interests_form'),
]
