from django.urls import path
from . import views

app_name = 'vendor_dashboard'

urlpatterns = [
    path('', views.VendorDashboard.as_view(), name = "vendor_dashboard"),
    path('vendor/profile', views.VendorProfile.as_view(), name = "vendor_profile"),
    path('vendor/update_profile/', views.UpdateProfileView.as_view(), name='update_vendor_profile'),
    path('vendor/sell-product/', views.VendorSellProduct.as_view(), name='vendor_sell_product'),
    path('vendor/sell-request-list/', views.VendorSellRequests.as_view(), name='vendor_sell_requests'),
]
