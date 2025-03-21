from django.urls import path
from . import views,api_views
from .manage_users import users
from .manage_gallery import media

from admin_dashboard.orders import order
from .manage_blogs import blogs
from .manage_newsactivity import newsactivity

from .registration import rtg_registration,vendor_registration,sp_registration
from .user_query import Query


app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboard.as_view(), name = "admin_dashboard"),
    path('city/<str:city_name>/', views.CityDetailView.as_view(), name='city_detail_view'),
    # manage users
    path('add_user',users.AddUser.as_view(), name='add_user'),
    path('pendingrtgs',users.PendingRtgs.as_view(), name='pending_rtg'),
    path('pendingvendors',users.PendingVendors.as_view(), name='pending_vendor'),
    path('pendingserviceproviders',users.PendingServiceProviders.as_view(), name='pending_service_provider'),
    path('quiz_answers/<int:user_id>',users.QuizAnswers.as_view(), name='quizanswers'),
    path('approve_user/<int:pk>',users.ApproveUser, name='approve_user'),
    path('reject_user/<int:pk>',users.RejectUser, name='reject_user'),
    path('rejected_rtgs/', users.RejectedRtgs.as_view(), name='rejected_rtgs'),
    path('rejected_vendors/', users.RejectedVendors.as_view(), name='rejected_vendors'),
    path('rejected_serviceproviders/', users.RejectedServiceProviders.as_view(), name='rejected_serviceproviders'),
    
    path('manage_users/serviceproviders_list',users.ServiceProvidersList.as_view(), name= 'serviceproviders_list'),
    path('manage_users/RTgardeners_list',users.RTGList.as_view(), name= 'RTgardeners_list'),
    path('manage_users/vendors_list',users.VendorList.as_view(), name= 'vendors_list'),
    path('manage_users/delete_rtg/<int:pk>',users.Delete_Rtg, name= 'delete_rtg'),
    path('manage_users/delete_vendor/<int:pk>',users.Delete_Vendor, name= 'delete_vendor'),
    path('manage_users/delete_serviceprovider/<int:pk>',users.Delete_Serviceprovider, name= 'delete_serviceprovider'),

    path('manage_users/users_gardening_data/<int:pk>',users.UserGardeningDetails.as_view(), name= 'gardening_details'),
    path('manage_users/vendor_data/<int:pk>',users.VendorDetails.as_view(), name= 'vendor_details'),
    path('manage_users/service_provider_data/<int:pk>',users.ServiceProviderDetails.as_view(), name= 'service_providor_details'),
    path('manage_users/search_user/rtg',users.RtgSearchUser.as_view(), name= 'search_user_rtg'),
    path('manage_users/search_user/vendor',users.VendorSearchUser.as_view(), name= 'search_user_vendor'),
    path('manage_users/search_user/sp',users.SpSearchUser.as_view(), name= 'search_user_sp'),

    path('manage_users/search_user/rtg/pending',users.PendingRtgSearch.as_view(), name= 'search_user_rtg_pending'),
    path('manage_users/search_user/vendor/pending',users.PendingVendorSearch.as_view(), name= 'search_user_vendor_pending'),
    path('manage_users/search_user/sp/pending',users.PendingSpSearch.as_view(), name= 'search_user_sp_pending'),

    path('manage_users/search_g_p_update_request',users.SearchGardeningProfileUpdateRequest.as_view(), name= 'search_gardening_profile_update_request'),
    path('manage_users/search_activity_request',users.SearchUsersActivityRequest.as_view(), name= 'search_activity_request'),
    path('manage_users/search_sell_produce_request',users.SearchProduceSellRequest.as_view(), name= 'search_produce_sell_request'),

    path('manage_users/rtg/add_wallet_balance',users.RtgWalletBalanceAdd.as_view(), name= 'rtg_add_wallet_balance'),
    path('manage_users/vendor/add_wallet_balance',users.VendorWalletBalanceAdd.as_view(), name= 'vendor_add_wallet_balance'),
    path('gardeningprofileupdaterequest',users.UserGardeningProfileUpdateRequest.as_view(), name= 'gardeningprofileupdaterequest'),
    path('approveprofie/<int:pk>',users.ApproveProfile, name= 'approveprofie'),
    path('rejectprofile',users.RejectProfile, name= 'rejectprofile'),
    path('useractivityrequest',users.UserActivityRequest.as_view(), name= 'useractivityrequest'),
    path('approveactivity/<int:pk>',users.ApproveActivity, name= 'approveactivity'),
    path('rejectactivity',users.RejectActivity, name= 'rejectpactivity'),
    path('sellrequest',users.UserProduceSellRequest.as_view(), name= 'sellrequest'),
    path('approvesellrequest',users.ApproveSellRequest, name= 'approvesellrequest'),
    path('rejectsellrequest',users.RejectSellRequest, name= 'rejectpsellrequest'),
    #Orders
    path('order/produce_order_list', order.ProduceOrderList.as_view(), name='produce_order_list'),
    path('order/produce_order_search', order.ProduceOrderSearch.as_view(), name='produce_order_search'),
    path('order/produce_order_detail/<str:order_id>', order.ProduceOrderDetail.as_view(), name='produce_order_detail'),
    path('order/download_produce_order_invoice/<str:order_id>', order.DownloadProduceOrderInvoice.as_view(), name='download_produce_order_invoice'),
    path('order/produce_order_status_search', order.ProduceOrderStatusSearch.as_view(), name='produce_order_status_search'),

    # API---------------
    # path('pending-users/', api_views.PendingUserAPIView.as_view(), name='api_pending_users'),
    # path('approve-user/<int:pk>/', api_views.ApproveUserAPIView.as_view(), name='api_approve_user'),
    # path('reject-user/<int:pk>/', api_views.RejectUserAPIView.as_view(), name='api_reject_user'),
    # path('user-gardening-details/<int:pk>/', api_views.UserGardeningDetailsAPIView.as_view(), name='api_user_gardening_details'),
    # path('vendor-details/<int:pk>/', api_views.VendorDetailsAPIView.as_view(), name='api_vendor_details'),
    # path('service-provider-details/<int:pk>/', api_views.ServiceProviderDetailsAPIView.as_view(), name='api_service_provider_details'),
    # path('quiz-answers/<int:user_id>/', api_views.QuizAnswersAPIView.as_view(), name='api_quiz_answers'),

    # Manage Blogs
    path('blogs_list',blogs.AllBlogsFromUsers.as_view(), name='blogs_list'),
    path('approve_blog/<int:blog_id>',blogs.ApproveBlog.as_view(), name='blogs_approve'),
    path('reject_blog/<int:blog_id>',blogs.DeclineBlog.as_view(), name='blog_reject'),
    path('delete_blog/<int:blog_id>',blogs.DeleteBlog.as_view(), name='blog_delete'),
    path('blog_search/',blogs.BlogSearch.as_view(), name='blog_search'),
    path('blog_update/<int:blog_id>',blogs.BlogUpdate.as_view(), name='blog_update'),

    # Registration

    path('add_rtg/',rtg_registration.RtgRegistration.as_view(), name='add_rtg'),
    path('add_vendor/',vendor_registration.VendorRegistration.as_view(), name='add_vendor'),
    path('add_service_provider/',sp_registration.ServiceProviderRegistration.as_view(), name='add_service_provider'),

    # Categories produces
    path('produces_categories/',views.ProducesCategory.as_view(), name='produces_categories'),
    path('produces_category_add/',views.ProducesCategoryAdd.as_view(), name='produces_category_add'),
    path('produces_category_update/<int:category_id>',views.ProducescategoryUpdate.as_view(), name='produces_category_update'),
    path('produces_category_delete/<int:category_id>',views.DeleteProducesCategory.as_view(), name='produces_category_delete'),
    path('produces_category/',views.ProducesCategorySearch.as_view(), name='produces_category_search'),
    
    # Categories service provider
    path('services_categories/',views.ServicesCategory.as_view(), name='services_categories'),
    path('services_category_add/',views.ServiceCategoryAdd.as_view(), name='services_category_add'),
    path('services_category_update/<int:category_id>',views.ServiceCategoryUpdate.as_view(), name='services_category_update'),
    path('services_category_delete/<int:category_id>',views.DeleteServiceCategory.as_view(), name='services_category_delete'),
    path('services_category/',views.ServiceCategorySearch.as_view(), name='services_category_search'),

    # User Query
    path('users_query/list/',Query.UsersQueryList.as_view(), name='users_query_list'),
    path('users_query/reply/<int:id>/',Query.QueryReply.as_view(), name='query_reply'),
    path('users_query/delete/<int:id>/',Query.DeleteQuery.as_view(), name='query_delete'),

    # media 
    path('media-gallery/', media.MediaGalleryListView.as_view(), name='media_gallery_list'),
    path('media-gallery/delete/<int:pk>/', media.MediaGalleryDeleteView.as_view(), name='media_gallery_delete'),


    path("newsactivity_list", newsactivity.NewsActivityList.as_view(), name="newsactivity_list"),
    path("newsactivitySearch", newsactivity.NewsActivitySearch.as_view(), name="newsactivity_search"),
    path("newsactivityAdd", newsactivity.NewsActivityAdd.as_view(), name="newsactivity_add"),
    path("newsactivityUpdate/<str:newsactivity_id>", newsactivity.NewsActivityUpdate.as_view(), name="newsactivity_update"),
    path("newsactivityDelete/<str:newsactivity_id>", newsactivity.NewsActivityDelete.as_view(), name="newsactivity_delete"),

    #user
    path('newsactivityList/', newsactivity.NewsActivityCategory.as_view(), name='user_newsactivity_list'),
    path('newsactivityDetails/<slug:slug>/', newsactivity.NewsActivityDetails.as_view(), name='user_newsactivity_details'),

     #api
    path('api/newsactivity/', newsactivity.NewsActivityListAPIView.as_view(), name='newsactivity_category'),
    path('api/newsactivity/<slug:slug>/', newsactivity.NewsActivityDetailsAPIView.as_view(), name='newsactivity_details'),
    path('api/media-gallery/', media.GalleryAPIView.as_view(), name='gellery_api'),


]


#  admin_dashboard:users_list