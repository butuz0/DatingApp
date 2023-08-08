from django.urls import path
from . import views

app_name = 'conversations'

urlpatterns = [
    path('', views.all_conversations, name='all_conversations'),
    path('<conversation_id>/', views.conversation_detail, name='conversation_detail'),
]
