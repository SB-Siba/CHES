from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_common.urls")),
    path("admin_dashboard/", include("admin_dashboard.urls")),
    path("user_dashboard/", include("user_dashboard.urls")),
    path("chat/", include("chatapp.urls")),
    path("vendor_dashboard/", include("vendor_dashboard.urls")),
    path("service_provider/", include("serviceprovider.urls")),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#admin_dashboard