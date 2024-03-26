from django.urls import path
from . import views
from .manage_users import users

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.AdminDashboard.as_view(), name = "admin_dashboard"),

    # manage users
    path('add_user',users.AddUser.as_view(), name='add_user'),
    path('manage_users/users_list',users.UserList.as_view(), name= 'users_list'),
    path('manage_users/user_update/<str:user_id>',users.UserUpdate.as_view(), name= 'user_update'),
    path('manage_users/search_user',users.SearchUser.as_view(), name= 'search_user'),
    path('manage_users/add_wallet_balance',users.WalletBalanceAdd.as_view(), name= 'add_wallet_balance'),
]

#  admin_dashboard:users_list