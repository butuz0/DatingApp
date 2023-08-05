from django.urls import path
from . import views

app_name = 'people'

urlpatterns = [
    path('list/', views.list_people, name='list_people'),
]
