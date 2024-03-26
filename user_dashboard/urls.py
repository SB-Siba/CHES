from django.urls import path
from . import views

app_name = 'user_dashboard'

urlpatterns = [
    path('', views.UserDashboard.as_view(), name = "user_dashboard"),

]

#  user_dashboard:user_dashboard