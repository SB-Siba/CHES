from django.urls import path
from . import views

app_name = 'app_common'

urlpatterns = [
    path('', views.Login.as_view(), name = "login"),
    path('authentication/register', views.Register.as_view(), name = "register"),
    path('authentication/logout', views.Logout.as_view(), name = "logout"),
    path('index', views.Home.as_view(), name='index'),
    path('add-gardening-details', views.GardeningDetails.as_view(), name='gardeningdetails'),
    path('gardening-quiz', views.gardening_quiz_view, name='gardeningquiz'),
]

#   app_common:register