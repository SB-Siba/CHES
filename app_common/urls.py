from django.urls import path
from . import top_users_api, views,auth_api,api_of_rtg,api_of_serviceprovider,api_of_vendor,email_otp_api
from django.contrib.auth import views as auth_view
from . forms import PasswordChangeForm
app_name = 'app_common'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),

    path('authentication/login', views.Login.as_view(), name = "login"),
    path('authentication/register/<str:role>/', views.Register.as_view(), name = "register"),
    path('authentication/logout', views.Logout.as_view(), name = "logout"),
    path("passwordChange/",auth_view.PasswordChangeView.as_view(template_name = 'app_common/authentication/changepassword.html',form_class = PasswordChangeForm,success_url = '/passwordchangedone'),name='passwordchange'),
    path("passwordchangedone/",auth_view.PasswordChangeDoneView.as_view(template_name = 'app_common/authentication/changepassworddone.html'),name='passwordchangedone'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name = "forgot_password"),
    path('reset-password/<uuid:token>/', views.ResetPasswordView.as_view(), name='reset_password'),

    path('add-gardening-details/<str:u_email>', views.GardeningDetails.as_view(), name='gardeningdetails'),
    path('gardening-quiz/<str:u_email>', views.gardening_quiz_view, name='gardeningquiz'),
    path('add-vendor-details/<str:u_email>', views.VendorDetails.as_view(), name='vendordetails'),
    path('add-service-provider-details/<str:u_email>', views.ServiceProviderDetails.as_view(), name='serviceproviderdetails'),

    # URLS API VIEWS AUTHENTICATION
    path('api/register/', auth_api.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', auth_api.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', auth_api.LogoutAPIView.as_view(), name='api_logout'),

    path('api/forgot-password/', auth_api.ForgotPasswordAPIView.as_view(), name='forgot_password_api'),
    path('api/reset-password/<uidb64>/<token>/', auth_api.ResetPasswordAPIView.as_view(), name='password_reset_confirm_api'),

    path('api/gardening-details/<str:u_email>/', auth_api.GardeningDetailsAPIView.as_view(), name='api_gardening_details'),
    path('api/gardening-quiz/<str:u_email>/', auth_api.GardeningQuizAPIView.as_view(), name='api_gardening_quiz'),
    path('api/vendor-details/<str:u_email>/', auth_api.VendorDetailsAPIView.as_view(), name='api_vendor_details'),
    path('api/service-provider-details/<str:u_email>/', auth_api.ServiceProviderDetailsAPIView.as_view(), name='api_service_provider_details'),

    # ----------------------------- Roof Top Gardener ------------------------------------

    path('api/user/profile/', api_of_rtg.UserProfileAPIView.as_view(), name='user_profile_api'),
    path('api/user/profile/update/', api_of_rtg.UpdateProfileViewAPIView.as_view(), name='update_profile_api'),
    path('api/gardening-profile/', api_of_rtg.GardeningProfileAPIView.as_view(), name='gardening_profile_api'),
    path('api/update-gardening-profile/', api_of_rtg.UpdateGardeningProfileAPIView.as_view(), name='update_gardening_profile_api'),
    path('api/add-activity/', api_of_rtg.AddActivityRequestAPIView.as_view(), name='add_activity_request_api'),
    path('api/activity-list/', api_of_rtg.ActivityListAPIView.as_view(), name='activity_list_api'),
    path('api/sell-produce/', api_of_rtg.SellProduceAPIView.as_view(), name='sell_produce_api'),
    path('api/sell-produce-list/', api_of_rtg.SellProduceListAPIView.as_view(), name='sell_produce_list_api'),
    path('api/green-commerce-product-community/', api_of_rtg.GreenCommerceProductCommunityAPIView.as_view(), name='green_commerce_product_community_api'),
    path('api/buying-begins/<int:prod_id>/', api_of_rtg.BuyingBeginsAPIView.as_view(), name='buying_begins_api'),
    path('api/buy-begins-seller/', api_of_rtg.BuyBeginsSellerAPIView.as_view(), name='buy_begins_seller_api'),
    path('api/buy-begins-buyer/', api_of_rtg.BuyBeginsBuyerAPIView.as_view(), name='buy_begins_buyer_api'),
    path('api/send-payment-link/<int:buy_id>/', api_of_rtg.SendPaymentLinkAPIView.as_view(), name='send_payment_link_api'),
    path('api/reject-buy/<int:ord_id>/', api_of_rtg.RejectBuyAPIView.as_view(), name='reject_buy_api'),
    path('api/produce-buy/<int:prod_id>/', api_of_rtg.ProduceBuyAPIView.as_view(), name='produce_buy_api'),
    path('api/all-orders/', api_of_rtg.AllOrdersAPIView.as_view(), name='all_order_api'),
    path('api/all-posts/', api_of_rtg.AllPostsAPIView.as_view(), name='all_posts_api'),
    path('api/posts/plus-like/', api_of_rtg.PlusLikeAPIView.as_view(), name='plus_like_api'),
    path('api/posts/minus-like/', api_of_rtg.MinusLikeAPIView.as_view(), name='minus_like_api'),
    path('api/posts/give-comment/', api_of_rtg.GiveCommentAPIView.as_view(), name='give_comment_api'),
    path('api/delete/comments/<int:post_id>/<str:comment_id>/', api_of_rtg.DeleteCommentAPIView.as_view(), name='delete_comment_api'),
    path('api/posts/get-all-comments/', api_of_rtg.GetAllCommentsAPIView.as_view(), name='get_all_comments_api'),
    path('api/rate-order/', api_of_rtg.RateOrderAPIView.as_view(), name='rate_order_api'),
    path('api/fetch-user-details/', api_of_rtg.FetchUserDetailsAPI.as_view(), name='fetch-user-details-api'),
    path('api/chat/', api_of_rtg.ChatAPI.as_view(), name='chat-api'),
    path('api/start-messages/<int:r_id>/', api_of_rtg.StartMessagesAPI.as_view(), name='start-messages-api'),
    path('api/send-message/', api_of_rtg.SendMessageApi.as_view(), name='send-message-api'),
    path('api/fetch-messages/', api_of_rtg.FetchMessageApi.as_view(), name='fetch-messages-api'),

    path('api/vendor-products/', api_of_rtg.VendorsProductsAPI.as_view(), name='vendor_products_api'),
    path('api/service-providers/', api_of_rtg.ServiceProvidersListAPIView.as_view(), name='service_providers_list'),

    path('api/checkout/<int:vprod_id>/<str:vendor_email>/', api_of_rtg.CheckoutAPIView.as_view(), name='checkout_api'),
    path('api/orders/from-vendors/', api_of_rtg.AllOrdersFromVendorsApi.as_view(), name='all_orders_from_vendors_api'),
    path('api/rate-order-from-vendor/', api_of_rtg.RateOrderFromVendorApi.as_view(), name='rate_order_from_vendor_api'),

    path('api/rtg/blogs/', api_of_rtg.BlogListAPIView.as_view(), name='blog-list'),
    path('api/rtg/blogs/add/', api_of_rtg.BlogAddAPIView.as_view(), name='blog-add'),
    path('api/rtg/blogs/<int:blog_id>/update/', api_of_rtg.BlogUpdateAPIView.as_view(), name='blog-update'),
    path('api/rtg/blogs/<int:blog_id>/delete/', api_of_rtg.BlogDeleteAPIView.as_view(), name='blog-delete'),
    path('api/rtg/blogs/view/', api_of_rtg.BlogViewAPIView.as_view(), name='blog-view'),
    path('api/rtg/blogs/<slug:slug>/', api_of_rtg.BlogDetailsAPIView.as_view(), name='blog-details'),

    path('api/rtg/list-of-services-by-service-provider/', api_of_rtg.ListOfServicesByServiceProvidersAPIView.as_view(), name='rtg_all_services_by_sp'),
    path('api/rtg/services/search/', api_of_rtg.ServiceSearchAPIView.as_view(), name='rtg_service_search'),
    path('api/rtg/services/<int:service_id>/', api_of_rtg.ServiceDetailsAPIView.as_view(), name='rtg_service_details'),
    path('api/rtg/my-booked-services/', api_of_rtg.MyBookedServicesAPIView.as_view(), name='rtg_my_booked_services'),
    path('api/rtg/bookings/<int:booking_id>/decline/', api_of_rtg.DeclineBookingAPIView.as_view(), name='rtg_decline_booking'),

    # ----------------------------- Service Provider ------------------------------------
    path('api/service_provider/profile/', api_of_serviceprovider.ServiceProviderProfileAPI.as_view(), name='service_provider_profile_api'),
    path('api/service-provider-profile/update/', api_of_serviceprovider.ServiceProviderUpdateProfileAPI.as_view(), name='update-service-provider-profile'),
    path('api/service-list/', api_of_serviceprovider.ServiceListAPIView.as_view(), name='service_list_api'),
    path('api/service-update/<int:service_id>/', api_of_serviceprovider.ServiceUpdateAPIView.as_view(), name='service_update_api'),
    path('api/service/<int:service_id>/delete/', api_of_serviceprovider.ServiceDeleteAPIView.as_view(), name='service_delete_api'),
    path('api/my_service_bookings/', api_of_serviceprovider.MyServiceBookingsAPIView.as_view(), name='my_service_bookings_api'),
    path('api/booking/<int:booking_id>/<str:action>/', api_of_serviceprovider.BookingActionAPIView.as_view(), name='booking_action_api'),
    
    path('api/sp/blogs/', api_of_serviceprovider.SpBlogListAPIView.as_view(), name='sp_blog_list_api'), 
    path('api/sp/blogs/add/', api_of_serviceprovider.SpBlogAddAPIView.as_view(), name='sp_blog_add_api'), 
    path('api/sp/blogs/<int:blog_id>/update/', api_of_serviceprovider.SpBlogUpdateAPIView.as_view(), name='sp_blog_update_api'), 
    path('api/sp/blogs/<int:blog_id>/delete/', api_of_serviceprovider.SpBlogDeleteAPIView.as_view(), name='sp_blog_delete_api'),
    path('api/sp/blogs/view/', api_of_serviceprovider.SpBlogViewAPIView.as_view(), name='sp_blog_view_api'),
    path('api/sp/blogs/<slug:slug>/details/', api_of_serviceprovider.SpBlogDetailsAPIView.as_view(), name='sp_blog_details_api'),
    
    # ----------------------------- Vendor ------------------------------------

    path('api/vendor/profile/', api_of_vendor.VendorProfileAPI.as_view(), name='vendor-profile-api'),
    path('api/vendor/update-profile/', api_of_vendor.VendorUpdateProfileAPIView.as_view(), name='vendor-update-profile-api'),
    path('api/vendor/gardening-profile/', api_of_vendor.VendorGardeningProfileAPIView.as_view(), name='vendor_gardening_profile_api'),
    path('api/vendor/update-gardening-profile/', api_of_vendor.VendorUpdateGardeningProfileAPIView.as_view(), name='vendor_update_gardening_profile_api'),
    
    path('api/vendor/sell-produce-list/', api_of_vendor.VendorSellProduceListAPIView.as_view(), name='vendor_sell_produce_list_api'),
    path('api/vendor/green-commerce-product-community/', api_of_vendor.VendorGreenCommerceProductCommunityAPIView.as_view(), name='vendor_green_commerce_product_community_api'),
    path('api/vendor/buying-begins/<int:prod_id>/', api_of_vendor.VendorBuyingBeginsAPIView.as_view(), name='vendor_buying_begins_api'),
    path('api/vendor/buy-begins-seller/', api_of_vendor.VendorBuyBeginsSellerAPIView.as_view(), name='vendor_buy_begins_seller_api'),
    path('api/vendor/buy-begins-buyer/', api_of_vendor.VendorBuyBeginsBuyerAPIView.as_view(), name='vendor_buy_begins_buyer_api'),
    path('api/vendor/send-payment-link/<int:buy_id>/', api_of_vendor.VendorSendPaymentLinkAPIView.as_view(), name='vendor_send_payment_link_api'),
    path('api/vendor/reject-buy/<int:ord_id>/', api_of_vendor.VendorRejectBuyAPIView.as_view(), name='vendor_reject_buy_api'),
    path('api/vendor/produce-buy/<int:prod_id>/', api_of_vendor.VendorProduceBuyAPIView.as_view(), name='vendor_produce_buy_api'),
    path('api/vendor/all-orders/', api_of_vendor.VendorAllOrdersAPIView.as_view(), name='vendor_all_order_api'),
    path('api/vendor/all-posts/', api_of_vendor.VendorAllPostsAPIView.as_view(), name='vendor_all_posts_api'),
    path('api/vendor/posts/plus-like/', api_of_vendor.VendorPlusLikeAPIView.as_view(), name='vendor_plus_like_api'),
    path('api/vendor/posts/minus-like/', api_of_vendor.VendorMinusLikeAPIView.as_view(), name='vendor_minus_like_api'),
    path('api/vendor/posts/give-comment/', api_of_vendor.VendorGiveCommentAPIView.as_view(), name='vendor_give_comment_api'),
    path('api/vendor/delete/comments/<int:post_id>/<str:comment_id>/', api_of_vendor.VendorDeleteCommentAPIView.as_view(), name='vendor_delete_comment_api'),
    path('api/vendor/posts/get-all-comments/', api_of_vendor.VendorGetAllCommentsAPIView.as_view(), name='vendor_get_all_comments_api'),
    path('api/vendor/rate-order/', api_of_vendor.VendorRateCommunityOrderAPIView.as_view(), name='vendor_rate_community_order_api'),
    path('api/vendor/fetch-user-details/', api_of_vendor.VendorFetchUserDetailsAPI.as_view(), name='vendor-fetch-user-details-api'),
    path('api/vendor/chat/', api_of_vendor.VendorChatAPI.as_view(), name='vendor-chat-api'),
    path('api/vendor/start-messages/<int:r_id>/', api_of_vendor.VendorStartMessagesAPI.as_view(), name='vendor-start-messages-api'),
    path('api/vendor/send-message/', api_of_vendor.VendorSendMessageApi.as_view(), name='vendor-send-message-api'),
    path('api/vendor/fetch-messages/', api_of_vendor.VendorFetchMessageApi.as_view(), name='vendor-fetch-messages-api'),
    
    path('api/vendor/sell-product/', api_of_vendor.VendorSellProductAPIView.as_view(), name='vendor-sell-product-api'),
    path('api/vendor/sold-products/', api_of_vendor.VendorSoldProductsAPIView.as_view(), name='vendor-sold-products-api'),
    path('api/vendor/sell-products-list/', api_of_vendor.SellProductsListAPIView.as_view(), name='vendor-sell-products-list-api'),
    path('api/vendor/update-product/<int:product_id>/', api_of_vendor.UpdateProductAPIView.as_view(), name='update-product-api'),
    path('api/vendor/delete-product/<int:product_id>/', api_of_vendor.DeleteSellProductAPIView.as_view(), name='delete-product-api'),
    path('api/vendor/add-activity/', api_of_vendor.AddActivityRequestVendorAPIView.as_view(), name='vendor-add_activity_request_api'),
    path('api/vendor/activity-list/', api_of_vendor.ActivityListVendorAPIView.as_view(), name='vendor_activity_list_api'),
    path('api/vendor/order/<str:order_uid>/', api_of_vendor.OrderDetailAPIView.as_view(), name='vendor_order_detail_api'),

    path('vendor/blogs/', api_of_vendor.VendorBlogListAPIView.as_view(), name='vendor-blog-list'),
    path('vendor/blogs/add/', api_of_vendor.VendorBlogAddAPIView.as_view(), name='vendor-blog-add'),
    path('vendor/blogs/<int:blog_id>/update/', api_of_vendor.VendorBlogUpdateAPIView.as_view(), name='vendor-blog-update'),
    path('vendor/blogs/<int:blog_id>/delete/', api_of_vendor.VendorBlogDeleteAPIView.as_view(), name='vendor-blog-delete'),
    path('vendor/blogs/view/', api_of_vendor.VendorBlogViewAPIView.as_view(), name='vendor-blog-view'),
    path('vendor/blogs/<slug:slug>/', api_of_vendor.VendorBlogDetailsAPIView.as_view(), name='vendor-blog-details'),

    path('api/vendor/list-of-services-by-service-provider/', api_of_vendor.ListOfServicesByServiceProvidersAPIView.as_view(), name='vendor_all_services_by_sp'),
    path('api/vendor/services/search/', api_of_vendor.ServiceSearchAPIView.as_view(), name='vendor_service_search'),
    path('api/vendor/services/<int:service_id>/', api_of_vendor.ServiceDetailsAPIView.as_view(), name='vendor_service_details'),
    path('api/vendor/my-booked-services/', api_of_vendor.MyBookedServicesAPIView.as_view(), name='vendor_my_booked_services'),
    path('api/vendor/bookings/<int:booking_id>/decline/', api_of_vendor.DeclineBookingAPIView.as_view(), name='vendor_decline_booking'),

    # OTP
    path('api/email/send-otp/', email_otp_api.SendOTPAPIView.as_view(), name='send_otp_api'),
    path('api/email/verify-otp/', email_otp_api.VerifyOTPAPIView.as_view(), name='verify_otp_api'), 

    #top Users
    path('api/top-users-rtg/', top_users_api.TopRTGUsersAPIView.as_view(), name='top_users_rtg'),
    path('api/top-users-vendor/', top_users_api.TopVendorUsersAPIView.as_view(), name='top_users_vendor'),

    # Category for produces
    path('api/produces/categories/', api_of_rtg.CategoryForProducesListView.as_view(), name='produces-category-list'),

    # Category for service provider
    path('api/services/spcategories/', api_of_rtg.CategoryForServiceProviderListView.as_view(), name='produces-spcategory-list'),
    #  User Query
    path('api/user/query/', api_of_rtg.UserQueryCreateView.as_view(), name='user-query-api'),

    path('api/privacy-policy/', auth_api.PrivacyPolicyAPIView.as_view(), name='privacy-policy-api'),
    path('api/about-us/', auth_api.AboutUsAPIView.as_view(), name='about-us-api'),
    path('api/terms-and-conditions/', auth_api.TermsAndConditionsAPIView.as_view(), name='terms-and-conditions-api'),

]