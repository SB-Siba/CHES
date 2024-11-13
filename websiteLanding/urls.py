from django.urls import path
from . import views

app_name = 'website_landing'

urlpatterns = [
    path('', views.WebsiteLanding.as_view(), name = "website_landing"),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),  

]
