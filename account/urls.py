from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.user_registration, name='user_register'),
    path('profile_register/', views.profile_registration, name='profile_register'),
]
