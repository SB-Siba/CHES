from django.urls import path
from . import views

app_name = 'vendor_dashboard'

urlpatterns = [
    path('', views.VendorDashboard.as_view(), name = "vendor_dashboard"),
    path('vendor/profile', views.VendorProfile.as_view(), name = "vendor_profile"),
    path('vendor/update_profile/', views.UpdateProfileView.as_view(), name='update_vendor_profile'),
    path('vendor/sell-product/', views.VendorSellProduct.as_view(), name='vendor_sell_product'),
    path('vendor/sell-request-list/', views.VendorSellRequests.as_view(), name='vendor_sell_requests'),
    path('vendor/sold-products-list/', views.VendorSoldProducts.as_view(), name='vendor_sold_products'),
    path('invoice/<int:order_uid>',views.VendorDownloadInvoice.as_view(),name="invoice"),
    path('addactivity', views.AddActivityVendor.as_view(), name = "addactivity"),
    path('activitylist', views.ActivityList.as_view(), name = "activitylist"),
    path('all-posts/', views.AllPosts.as_view(), name = "allposts"),
    path("pluslike/",views.plus_like,name="like"),
    path('minuslike/',views.minus_like,name="dislike"),
    path('give-comment/',views.give_comment,name="give_comment"),
    path('all-comment/',views.get_all_comments,name="get_all_comments"),
    path('walletpage', views.WalletView.as_view(), name = "walletpage"),

    path('sellproduce', views.SellProduceView.as_view(), name = "sellproduce"),
    path('allsellrequests', views.AllSellRequests.as_view(), name = "allsellrequests"),

    path('greencommerceproducts', views.GreenCommerceProductCommunity.as_view(), name = "greencommerceproducts"),
    path('buyingbegins/<int:prod_id>', views.BuyingBegins.as_view(), name = "buybegins"),
    path('buybeginssellerview', views.BuyBeginsSellerView.as_view(), name = "buybeginssellerview"),
    path('sendpaymentlink/<int:buy_id>', views.send_payment_link, name = "sendpaymentlink"),
    path('buybeginsbuyerview', views.BuyBeginsBuyerView.as_view(), name = "buybeginsbuyerview"),
    path('producebuy/<int:prod_id>', views.ProduceBuyView.as_view(), name = "producebuy"),
    path('buyreject/<int:ord_id>', views.reject_buy, name = "buyreject"),
    path('orders/', views.AllOrders.as_view(), name = "allorders"),
]
