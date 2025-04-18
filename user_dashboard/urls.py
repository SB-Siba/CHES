from django.urls import path
from . import views

app_name = 'user_dashboard'

urlpatterns = [
    path('', views.UserDashboard.as_view(), name = "user_dashboard"),
    path('userprofile', views.UserProfile.as_view(), name = "userprofile"),
    path('gardeningprofile', views.GardeningProfile.as_view(), name = "gardeningprofile"),
    path('userprofileupdate', views.UpdateProfileView.as_view(), name = "userprofileupdate"),
    path('gardeningprofileupdate', views.UpdateGardeningProfileView.as_view(), name = "gardeningprofileupdate"),
    path('addactivity', views.AddActivityRequest.as_view(), name = "addactivity"),
    path('activitylist', views.ActivityList.as_view(), name = "activitylist"),

    path('walletpage', views.WalletView.as_view(), name = "walletpage"),
    path('privacypolicy', views.PrivacyPolicyPage.as_view(), name = "privacypolicy"),
    path('servicepage', views.ServicePage.as_view(), name = "servicepage"),
    path('contactpage', views.ContactePage.as_view(), name = "contactpage"),

    path('sellproduce', views.SellProduceView.as_view(), name = "sellproduce"),
    path('produces/', views.ProduceListView.as_view(), name='produce_list'),
    path('produces/<int:pk>/edit/', views.UpdateProduceView.as_view(), name='update_produce'),
    path('produces/<int:pk>/delete/', views.DeleteProduceView.as_view(), name='delete_produce'),
    path('allsellrequests', views.AllSellRequests.as_view(), name = "allsellrequests"),

    path('greencommerceproducts', views.GreenCommerceProductCommunity.as_view(), name = "greencommerceproducts"),
    path('buyingbegins/<int:prod_id>', views.BuyingBegins.as_view(), name = "buybegins"),
    path('buybeginssellerview', views.BuyBeginsSellerView.as_view(), name = "buybeginssellerview"),
    path('sendpaymentlink/<int:buy_id>', views.send_payment_link, name = "sendpaymentlink"),
    path('buybeginsbuyerview', views.BuyBeginsBuyerView.as_view(), name = "buybeginsbuyerview"),
    path('producebuy/<int:prod_id>', views.ProduceBuyView.as_view(), name = "producebuy"),
    path('buyreject/<int:ord_id>', views.reject_buy, name = "buyreject"),
    path('orders/', views.AllOrders.as_view(), name = "allorders"),
    path('all-posts/', views.AllPosts.as_view(), name = "allposts"),
    path("pluslike/",views.plus_like,name="like"),
    path('minuslike/',views.minus_like,name="dislike"),
    path('give-comment/',views.give_comment,name="give_comment"),
    path('delete_comment/<int:post_id>/<str:comment_id>/', views.delete_comment, name='delete_comment'),
    path('all-comment/',views.get_all_comments,name="get_all_comments"),
    path('rate-order/',views.RateOrder.as_view(),name="rate_order"),

    path('products-from-vendor/', views.VendorsProduct.as_view(), name = "vendorproducts"),
    path('checkout-vendor-products/<int:vprod_id>/<str:vendor_email>/', views.CheckoutView.as_view(), name="checkout_vendor_products"),
    path('orders-from-vendor/', views.AllOrdersFromVendors.as_view(), name = "allordersfromvendor"),
    path('invoice/<int:order_uid>',views.GardenerDownloadInvoice.as_view(),name="invoice"),
    path('rate-order-from-vendor/',views.RateOrderFromVendor.as_view(),name="rate_order_from_vendor"),

    path('service/service_search', views.ServiceSearchView.as_view(), name='service_search'),
    path('services/', views.ListOfServicesByServiceProviders.as_view(), name='list_services'),
    path('service_details/<int:service_id>/', views.ServiceDetails.as_view(), name='service_details'),
    path('my_booked_services/', views.MyBookedServices.as_view(), name='my_booked_services'),
    path('rtg/decline_booking/<int:booking_id>', views.rtg_decline_booking, name='rtg_decline_booking'),
    path('ExploreGreenCommerce/', views.ExploreGreenCommerce.as_view(), name='ExploreGreenCommerce'),
    # path('checkout/<int:vprod_id>/<str:vendor_email>/', views.CheckoutView.as_view(), name='checkout'),
    # path('payment-confirmation/', views.PaymentConfirmationView.as_view(), name='payment_confirmation'),

    # path('payment/<int:order_id>/', views.PaymentPageView.as_view(), name='payment_page'),

]

#  user_dashboard:user_dashboard