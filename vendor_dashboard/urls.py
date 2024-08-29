from django.urls import path
from . import views

app_name = 'vendor_dashboard'

urlpatterns = [
    path('', views.VendorDashboard.as_view(), name = "vendor_dashboard"),
    path('vendor/profile', views.VendorProfile.as_view(), name = "vendor_profile"),
    path('vendor/update_profile/', views.UpdateProfileView.as_view(), name='update_vendor_profile'),
    path('vendor/sell-product/', views.VendorSellProduct.as_view(), name='vendor_sell_product'),
    path('vendor/sell-product-list/', views.SellProductsList.as_view(), name='vendor_sell_product_list'),
    path('vendor/sell-product-update/<int:product_id>', views.UpdateProduct.as_view(), name='vendor_sell_product_update'),
    path('vendor/sell-product-delete/<int:product_id>', views.DeleteSellProduct.as_view(), name='vendor_sell_product_delete'),
    path('vendor/sold-products-list/', views.VendorSoldProducts.as_view(), name='vendor_sold_products'),
    path('invoice/<int:order_uid>',views.VendorDownloadInvoice.as_view(),name="invoice"),
    path('addactivity', views.AddActivityVendor.as_view(), name = "addactivity"),
    path('activitylist', views.ActivityList.as_view(), name = "activitylist"),
    path('all-posts/', views.AllPosts.as_view(), name = "allposts"),
    path("pluslike/",views.plus_like,name="like"),
    path('minuslike/',views.minus_like,name="dislike"),
    path('give-comment/',views.give_comment,name="give_comment"),
    path('delete_comment/<int:post_id>/<str:comment_id>/', views.delete_comment, name='delete_comment'),
    path('all-comment/',views.get_all_comments,name="get_all_comments"),
    path('walletpage', views.WalletView.as_view(), name = "walletpage"),
    path('my-community-orders/', views.Mycommunityorders.as_view(), name = "allorderscommunity"),
    path('rate-order/',views.RateOrder.as_view(),name="rate_order"),

    path('sellproduce', views.SellProduceView.as_view(), name = "sellproduce"),
    path('allsellrequests', views.AllSellRequests.as_view(), name = "allsellrequests"),

    path('greencommerceproducts', views.GreenCommerceProductCommunity.as_view(), name = "greencommerceproducts"),
    path('buyingbegins/<int:prod_id>', views.BuyingBegins.as_view(), name = "buybegins"),
    path('buybeginssellerview', views.BuyBeginsSellerView.as_view(), name = "buybeginssellerview"),
    path('sendpaymentlink/<int:buy_id>', views.send_payment_link, name = "sendpaymentlink"),
    path('buybeginsbuyerview', views.BuyBeginsBuyerView.as_view(), name = "buybeginsbuyerview"),
    path('producebuy/<int:prod_id>', views.ProduceBuyView.as_view(), name = "producebuy"),
    path('buyreject/<int:ord_id>', views.reject_buy, name = "buyreject"),
    #Orders
    path('order/vendor_order_list', views.AllOrders.as_view(), name='vendor_order_list'),
    path('order/vendor_order_search', views.OrderSearch.as_view(), name='vendor_order_search'),
    path('order/order_detail/<str:order_uid>', views.OrderDetail.as_view(), name='order_detail'),
    path('order/order_status_search', views.OrderStatusSearch.as_view(), name='order_status_search'),

    path('service-providers-list/',views.ServiceProvidersList.as_view(),name="service_providers"),
    path('service/service_search', views.ServiceSearchView.as_view(), name='service_search'),
    path('services/', views.ListOfServicesByServiceProviders.as_view(), name='list_services'),
    path('service_details/<int:service_id>/', views.ServiceDetails.as_view(), name='service_details'),
    path('my_booked_services/', views.MyBookedServices.as_view(), name='my_booked_services'),
    path('rtg/decline_booking/<int:booking_id>', views.vendor_decline_booking, name='vendor_decline_booking'),
]
