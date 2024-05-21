from django.urls import path
from . import views
from .manage_users import users

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboard.as_view(), name = "admin_dashboard"),

    # manage users
    path('add_user',users.AddUser.as_view(), name='add_user'),
    path('pendingusers',users.PendingUser.as_view(), name='pending_user'),
    path('quiz_answers/<int:user_id>',users.QuizAnswers.as_view(), name='quizanswers'),
    path('approve_user/<int:pk>',users.ApproveUser, name='approve_user'),
    path('reject_user/<int:pk>',users.RejectUser, name='reject_user'),
    path('manage_users/gardeners_list',users.GardenerList.as_view(), name= 'gardeners_list'),
    path('manage_users/vendors_list',users.VendorList.as_view(), name= 'vendors_list'),
    path('manage_users/delete_user/<int:pk>',users.Delete_User, name= 'delete_user'),

    path('manage_users/users_gardening_data/<int:pk>',users.UserGardeningDetails.as_view(), name= 'gardening_details'),
    path('manage_users/vendor_data/<int:pk>',users.VendorDetails.as_view(), name= 'vendor_details'),
    path('manage_users/user_update/<str:user_id>',users.UserUpdate.as_view(), name= 'user_update'),
    path('manage_users/search_user',users.SearchUser.as_view(), name= 'search_user'),
    path('manage_users/add_wallet_balance',users.WalletBalanceAdd.as_view(), name= 'add_wallet_balance'),
    path('gardeningprofileupdaterequest',users.UserGardeningProfileUpdateRequest.as_view(), name= 'gardeningprofileupdaterequest'),
    path('approveprofie/<int:pk>',users.ApproveProfile, name= 'approveprofie'),
    path('rejectprofile',users.RejectProfile, name= 'rejectprofile'),
    path('useractivityrequest',users.UserActivityRequest.as_view(), name= 'useractivityrequest'),
    path('approveactivity/<int:pk>',users.ApproveActivity, name= 'approveactivity'),
    path('rejectactivity',users.RejectActivity, name= 'rejectpactivity'),
    path('sellrequest',users.UserProduceSellRequest.as_view(), name= 'sellrequest'),
    path('approvesellrequest',users.ApproveSellRequest, name= 'approvesellrequest'),
    path('rejectsellrequest',users.RejectSellRequest, name= 'rejectpsellrequest'),




]

#  admin_dashboard:users_list