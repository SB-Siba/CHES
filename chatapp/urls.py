from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('user-info/', views.user_info, name='user-info'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<str:full_name>/', views.conversation_sender, name='conversation'),
    path('conversation_reciver/<str:full_name>/', views.conversation_reciver, name='conversation_reciver'),
    path('compose/<str:full_name>/', views.compose_message, name='compose_message'),
    path('all_messages', views.allMessages, name='all_messages'),
    # Other URLs for login, logout, registration, etc.
]