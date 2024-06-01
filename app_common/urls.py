from django.urls import path
from . import views

app_name = 'app_common'

urlpatterns = [
    path('', views.Login.as_view(), name = "login"),
    path('authentication/register', views.Register.as_view(), name = "register"),
    path('authentication/logout', views.Logout.as_view(), name = "logout"),
    path('index', views.Home.as_view(), name='index'),
    path('add-gardening-details/<str:u_email>', views.GardeningDetails.as_view(), name='gardeningdetails'),
    path('gardening-quiz/<str:u_email>', views.gardening_quiz_view, name='gardeningquiz'),
    path('add-vendor-details/<str:u_email>', views.VendorDetails.as_view(), name='vendordetails'),
    path('add-service-provider-details/<str:u_email>', views.ServiceProviderDetails.as_view(), name='serviceproviderdetails'),
]

#   app_common:register