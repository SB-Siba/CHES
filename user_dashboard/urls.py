from django.urls import path
from . import views

app_name = 'user_dashboard'

urlpatterns = [
    path('', views.UserDashboard.as_view(), name = "user_dashboard"),
    path('userprofile', views.UserProfile.as_view(), name = "userprofile"),
    path('gardeningprofile', views.GardeningProfie.as_view(), name = "gardeningprofile"),
    path('userprofileupdate', views.UpdateProfileView.as_view(), name = "userprofileupdate"),
    path('gardeningprofileupdate', views.UpdateGardeningProfileView.as_view(), name = "gardeningprofileupdate"),
    path('addactivity', views.AddActivityRequest.as_view(), name = "addactivity"),
    path('activitylist', views.ActivityList.as_view(), name = "activitylist"),

    path('walletpage', views.WalletView.as_view(), name = "walletpage"),
    path('privacypolicy', views.PrivacyPolicyPage.as_view(), name = "privacypolicy"),
    path('servicepage', views.ServicePage.as_view(), name = "servicepage"),
    path('contactpage', views.ContactePage.as_view(), name = "contactpage"),

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
    path('all-posts/', views.AllPosts.as_view(), name = "allposts"),
    path("pluslike/",views.plus_like,name="like"),
    path('minuslike/',views.minus_like,name="dislike"),
    path('give-comment/',views.give_comment,name="give_comment"),
    path('all-comment/',views.get_all_comments,name="get_all_comments"),
    path('rate-order/',views.RateOrder.as_view(),name="rate_order"),
]

#  user_dashboard:user_dashboard