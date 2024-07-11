from django.urls import path
from . import views,auth_api,api_of_rtg,api_of_serviceprovider
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
    path('password-reset/', views.CustomPasswordResetView.as_view(),name='password-reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',views.CustomPasswordResetCompleteView.as_view(),name='password_reset_complete'),

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

    # ----------------------------- Service Provider ------------------------------------
    path('api/service_provider/profile/', api_of_serviceprovider.ServiceProviderProfileAPI.as_view(), name='service_provider_profile_api'),
    path('api/service-provider-profile/update/', api_of_serviceprovider.ServiceProviderUpdateProfileAPI.as_view(), name='update-service-provider-profile'),
    path('api/service-list/', api_of_serviceprovider.ServiceListAPIView.as_view(), name='service_list_api'),
    path('api/service-update/<int:service_id>/', api_of_serviceprovider.ServiceUpdateAPIView.as_view(), name='service_update_api'),
    path('api/service/<int:service_id>/delete/', api_of_serviceprovider.ServiceDeleteAPIView.as_view(), name='service_delete_api'),
    path('api/my_service_bookings/', api_of_serviceprovider.MyServiceBookingsAPIView.as_view(), name='my_service_bookings_api'),
    path('api/booking/<int:booking_id>/<str:action>/', api_of_serviceprovider.BookingActionAPIView.as_view(), name='booking_action_api'),

]

#   app_common:register