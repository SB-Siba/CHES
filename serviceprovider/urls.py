from django.urls import path
from . import views

app_name = 'service_provider'

urlpatterns = [
    path('', views.ServiceProviderDashboard.as_view(), name = "service_provider_dash"),
    path('service_provider/profile', views.ServiceProviderProfile.as_view(), name = "service_provider_profile"),
    path('service_provider/update_profile/', views.ServiceProviderUpdateProfileView.as_view(), name='update_service_provider_profile'),
]
