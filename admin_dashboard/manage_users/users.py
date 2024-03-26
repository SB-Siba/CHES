from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings

from helpers import utils
from app_common import models
from .import forms
from app_common.forms import RegisterForm

app = "admin_dashboard/manage_users/"

class UserList(View):
    template = app + "user_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        page = request.GET.get('page',1)

        user_list= self.model.objects.all().order_by("-id")
        paginated_data = utils.paginate(request, user_list, 25, page)
        context = {
            "user_list":paginated_data,
            'data_list':paginated_data,
            'form':self.form_class,
        }
        return render(request, self.template, context)
    
class SearchUser(View):
    model = models.User
    template = app + "user_list.html"
    
    def get(self, request):
        raw_query_dict = request.GET.dict()
        query_dict =(lambda query_dict: {f'{query_dict["search_by"]}':f'{query_dict["query"]}'})(raw_query_dict)

        # user = self.model.objects.filter()
        user_list= self.model.objects.filter(**query_dict)
        print(user_list)
        paginated_data = utils.paginate(request, user_list, 25, 1)
        context = {
            "user_list":paginated_data,
            'data_list':paginated_data,
        }
        return render(request, self.template, context)
    

class WalletBalanceAdd(View):
    model = models.User
    template = app + "wallet_balance_add.html"
    form_class = forms.WalletBalanceAdd

    def post(self, request):
        user_obj = self.model.objects.get(id = request.POST.get('user_id'))
        user_obj.wallet = user_obj.wallet + float(request.POST.get('wallet'))
        user_obj.save()
        messages.success(request, 'Wallet balance is updated')
        
        return redirect("admin_dashboard:users_list")
    

class UserUpdate(View):
    model = models.User
    template = app + "user_update.html"
    form_class = forms.UserEdit

    def get(self, request, user_id):
        user_obj = self.model.objects.get(id = user_id)
        context = {
            "form": self.form_class(instance= user_obj),
            "user_id" : user_id,
        }
        return render( request, self.template, context)
    
    def post(self, request, user_id):
        user_obj = self.model.objects.get(id = user_id)
        form = self.form_class(request.POST, instance= user_obj)

        if form.is_valid():
            form.save()
            messages.success(request, 'User is updated successfully....')
            return redirect('admin_dashboard:users_list')
        
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

            return redirect('admin_dashboard:user_update', user_id = user_id)
        

class AddUser(View):
    model = models.User
    template = app + "add_user.html"
    form_class = forms.UserAddForm

    def get(self, request):
        context = {
            "form": self.form_class,
        }
        return render( request, self.template, context)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account is created successfully')
            return redirect('admin_dashboard:users_list')
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

            context = {
            "form": self.form_class(data=request.POST),
            }
            return render( request, self.template, context)