from django.urls import path
from . import views

app_name = 'service_provider'

urlpatterns = [
    path('', views.ServiceProviderDashboard.as_view(), name = "service_provider_dash"),
    path('service_provider/profile', views.ServiceProviderProfile.as_view(), name = "service_provider_profile"),
    path('service_provider/update_profile/', views.ServiceProviderUpdateProfileView.as_view(), name='update_service_provider_profile'),
    path('service_provider/service_list', views.ServiceList.as_view(), name = "service_list"),
    path("service_provider/service_update/<int:service_id>", views.ServiceUpdate.as_view(), name="service_update"),
    path("service_provider/service_delete/<int:service_id>", views.ServiceDelete.as_view(), name="service_delete"),
    path('my_all_bookings/', views.MyServiceBookings.as_view(), name='my_all_bookings'),
    path('bookings/confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('bookings/cancel/<int:booking_id>/', views.decline_booking, name='decline_booking'),
    path('bookings/mark_as_complete/<int:booking_id>/', views.mark_as_complete_booking, name='mark_as_complete'),
]
