from django.urls import path
from . rtg_views import views as rtgBlogs
from . vendor_views import views as vendorBlogs
from . service_provider_views import views as spBlogs
from .admin_views import views as adminBlogs

app_name = 'blogs'

urlpatterns = [
    path("rtg_blog_list", rtgBlogs.BlogList.as_view(), name="rtg_blog_list"),
    path("rtg_blog_add", rtgBlogs.BlogAdd.as_view(), name="rtg_blog_add"),
    path("rtg_blog_update/<str:blog_id>", rtgBlogs.BlogUpdate.as_view(), name="rtg_blog_update"),
    path("rtg_blog_delete/<str:blog_id>", rtgBlogs.BlogDelete.as_view(), name="rtg_blog_delete"),
    path('rtg_all_blogs/', rtgBlogs.BlogView.as_view(), name='rtg_all_blogs'),
    path('rtg_blog_details/<slug:slug>/', rtgBlogs.BlogDetails.as_view(), name='rtg_blog_details'),
    path("rtg_blog_search", rtgBlogs.BlogSearch.as_view(), name="rtg_blog_search"),
    # Vendor
    path("vendor_blog_list", vendorBlogs.VendorBlogList.as_view(), name="vendor_blog_list"),
    path("vendor_blog_add", vendorBlogs.VendorBlogAdd.as_view(), name="vendor_blog_add"),
    path("vendor_blog_update/<str:blog_id>", vendorBlogs.VendorBlogUpdate.as_view(), name="vendor_blog_update"),
    path("vendor_blog_delete/<str:blog_id>", vendorBlogs.VendorBlogDelete.as_view(), name="vendor_blog_delete"),
    path('vendor_all_blogs/', vendorBlogs.VendorBlogView.as_view(), name='vendor_all_blogs'),
    path('vendor_blog_details/<slug:slug>/', vendorBlogs.VendorBlogDetails.as_view(), name='vendor_blog_details'),
    path("vendor_blog_search", vendorBlogs.VendorBlogSearch.as_view(), name="vendor_blog_search"),

    # Sp
    path("sp_blog_list", spBlogs.SpBlogList.as_view(), name="sp_blog_list"),
    path("sp_blog_add", spBlogs.SpBlogAdd.as_view(), name="sp_blog_add"),
    path("sp_blog_update/<str:blog_id>", spBlogs.SpBlogUpdate.as_view(), name="sp_blog_update"),
    path("sp_blog_delete/<str:blog_id>", spBlogs.SpBlogDelete.as_view(), name="sp_blog_delete"),
    path('sp_all_blogs/', spBlogs.SpBlogView.as_view(), name='sp_all_blogs'),
    path('sp_blog_details/<slug:slug>/', spBlogs.SpBlogDetails.as_view(), name='sp_blog_details'),
    path("sp_blog_search", spBlogs.SpBlogSearch.as_view(), name="sp_blog_search"),

    # Admin
    path("admin_blog_add", adminBlogs.AdminBlogAdd.as_view(), name="admin_blog_add"),
    path("admin_blog_list", adminBlogs.AdminBlogList.as_view(), name="admin_blog_list"),
    path("admin_blog_update/<str:blog_id>", adminBlogs.AdminBlogUpdate.as_view(), name="admin_blog_update"),
    path("admin_blog_delete/<str:blog_id>", adminBlogs.AdminBlogDelete.as_view(), name="admin_blog_delete"),
    path('admin_all_blogs/', adminBlogs.AdminBlogView.as_view(), name='admin_all_blogs'),
    path('admin_blog_details/<slug:slug>/', adminBlogs.AdminBlogDetails.as_view(), name='admin_blog_details'),
    path("admin_blog_search", adminBlogs.AdminBlogSearch.as_view(), name="admin_blog_search"),

]
