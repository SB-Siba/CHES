from django.urls import path
from . rtg_views import views as rtgBlogs

app_name = 'blogs'

urlpatterns = [
    path("rtg_blog_list", rtgBlogs.BlogList.as_view(), name="rtg_blog_list"),
    path("rtg_blog_add", rtgBlogs.BlogAdd.as_view(), name="rtg_blog_add"),
    path("rtg_blog_update/<str:blog_id>", rtgBlogs.BlogUpdate.as_view(), name="rtg_blog_update"),
    path("rtg_blog_delete/<str:blog_id>", rtgBlogs.BlogDelete.as_view(), name="rtg_blog_delete"),
    path('rtg_all_blogs/', rtgBlogs.BlogView.as_view(), name='rtg_all_blogs'),
    path('rtg_blog_details/<slug:slug>/', rtgBlogs.BlogDetails.as_view(), name='rtg_blog_details'),
]
