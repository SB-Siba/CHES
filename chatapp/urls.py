from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('fetch_user_details/', views.fetch_user_details, name='fetch_user_details'),
    path('startmessages/<int:r_id>/<int:product_id>/', views.start_messages, name='startmessages'),
    path('fetch_messages/', views.fetch_messages, name='fetch_messages'),
    path('send_message/', views.send_message, name='send_message'),
    path('all_messages', views.chat, name='all_messages'),
]