from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from EmailIntigration.views import send_template_email
from helpers import utils
from app_common import models
from .import forms
from app_common.forms import RegisterForm
from django.shortcuts import get_object_or_404

app = "admin_dashboard/manage_users/"


class PendingRtgs(View):
    model = models.User
    template = app + "forapprovertg.html"
    
    def get(self, request):
        not_approvedlist = self.model.objects.filter(is_approved=False,is_rtg = True).order_by('-id')
        rtgardener_list = []  
        rtgarden_details_list = []
        try:
            for i in not_approvedlist:
                rtgardener_list.append(i)
                garden_details = models.GardeningProfile.objects.get(user = i)
                rtgarden_details_list.append(garden_details)
            rtgardener_data = zip(rtgardener_list,rtgarden_details_list)
        except Exception:
            rtgardener_list = []
            rtgarden_details_list = []
            rtgardener_data = zip(rtgardener_list,rtgarden_details_list)
        return render(request,self.template,locals())
    
class PendingVendors(View):
    model = models.User
    template = app + "forapprovevendor.html"
    
    def get(self, request):
        not_approvedlist = self.model.objects.filter(is_approved=False,is_vendor = True).order_by('-id')
        vendor_list = []
        vendor_details_list = []
        try:
            for i in not_approvedlist:
                vendor_list.append(i)
                vendor_details = models.VendorDetails.objects.get(vendor = i)
                vendor_details_list.append(vendor_details)
            vendor_data = zip(vendor_list,vendor_details_list)
        except Exception:
            vendor_list = []
            vendor_details_list = []
            vendor_data = zip(vendor_list,vendor_details_list)
        return render(request,self.template,locals())
    
class PendingServiceProviders(View):
    model = models.User
    template = app + "forapproveserviceprovider.html"
    
    def get(self, request):
        not_approvedlist = self.model.objects.filter(is_approved=False,is_serviceprovider = True).order_by('-id')
        service_provider_list = []
        service_provider_details_list = []
        try:
            for i in not_approvedlist:
                service_provider_list.append(i)
                s_provider_details = models.ServiceProviderDetails.objects.get(provider = i)
                service_provider_details_list.append(s_provider_details)
            service_provider_data = zip(service_provider_list,service_provider_details_list)
        except Exception:
            service_provider_list = []
            service_provider_details_list = []
            service_provider_data = zip(service_provider_list,service_provider_details_list)
        return render(request,self.template,locals())
        
def ApproveUser(request, pk):
    user = get_object_or_404(models.User, id=pk)
    if user is not None:
        coins = request.GET.get('coins', None)
        user.is_approved = True
        if coins:
            user.wallet = 500 + int(coins)
        else:
            user.wallet = 500 + user.quiz_score
        user.coins = 100

        send_template_email(
            subject="Successful Approval",
            template_name="mail_template/successfull_approval_mail.html",
            context={'full_name': user.full_name,"email":user.email},
            recipient_list=[user.email]
        )

        user.save()
    else:
        msg = 'This account does not exist.'
        messages.error(request,msg)
    return redirect("admin_dashboard:admin_dashboard") 

def RejectUser(request, pk):
    user = get_object_or_404(models.User, id=pk)
    if user is not None:
        send_template_email(
            subject="Profile Rejected",
            template_name="mail_template/account_rejected_mail.html",
            context={'full_name': user.full_name,"email":user.email},
            recipient_list=[user.email]
        )
        user.delete()
    else:
        msg = 'This account does not exist.'
        messages.error(request,msg)
    return redirect("admin_dashboard:admin_dashboard") 

class ServiceProvidersList(View):
    template = app + "serviceprovider_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        page = request.GET.get('page',1)

        user_list= self.model.objects.filter(is_approved=True,is_superuser = False,is_serviceprovider = True).order_by("-id")
        paginated_data = utils.paginate(request, user_list, 25, page)
        context = {
            "user_list":paginated_data,
            'data_list':paginated_data,
            'form':self.form_class,
        }
        return render(request, self.template, context)
    
class RTGList(View):
    template = app + "rtg_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        page = request.GET.get('page',1)

        user_list= self.model.objects.filter(is_approved=True,is_superuser = False,is_rtg = True).order_by("-id")
        paginated_data = utils.paginate(request, user_list, 25, page)
        context = {
            "user_list":paginated_data,
            'data_list':paginated_data,
            'form':self.form_class,
        }
        return render(request, self.template, context)
class VendorList(View):
    template = app + "vendor_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        page = request.GET.get('page',1)

        user_list= self.model.objects.filter(is_approved=True,is_superuser = False,is_vendor = True).order_by("-id")
        paginated_data = utils.paginate(request, user_list, 25, page)
        context = {
            "user_list":paginated_data,
            'data_list':paginated_data,
            'form':self.form_class,
        }
        return render(request, self.template, context)
    
def Delete_User(request, pk):
    user = get_object_or_404(models.User, id=pk)
    # Checking if the logged in user can delete this user
    try:
        user.delete()
    except Exception as e:
        print(e)
    messages.success(request,"Successfully Deleted!")
    return redirect("admin_dashboard:users_list")


class UserGardeningDetails(View):
    template = app + "gardening_data.html"
    def get(self, request, pk):
        user = get_object_or_404(models.User, id=pk)
        gardening_data = get_object_or_404(models.GardeningProfile, user=user)

        return render(request, self.template, locals())
    
class VendorDetails(View):
    template = app + "vendor_data.html"
    def get(self, request, pk):
        user = get_object_or_404(models.User, id=pk)
        vendor_data = get_object_or_404(models.VendorDetails, vendor=user)

        return render(request, self.template, locals())
    
class ServiceProviderDetails(View):
    template = app + "service_provider_data.html"
    def get(self, request, pk):
        user = get_object_or_404(models.User, id=pk)
        serviceprovider_data = get_object_or_404(models.ServiceProviderDetails, provider=user)

        return render(request, self.template, locals())
    
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
        
class QuizAnswers(View):
    model = models.GaredenQuizModel
    template = app + "quiz_view.html"

    def get(self, request, user_id):
        user_obj = get_object_or_404(models.User, id = user_id)
        quiz = get_object_or_404(self.model, user=user_obj)
        user_id = user_id
        return render(request,self.template,locals())
    
    def post(self, request,user_id):
        user_id = user_id
        try:
            user_obj = get_object_or_404(models.User, id = user_id)
            quizPoints = request.POST['quizPoints']

            user_obj.quiz_score = int(quizPoints)
            user_obj.save()
            messages.success(request, 'Wallet Balance For Quiz Given Successfully')
            return redirect("admin_dashboard:pending_rtg")
        except models.User.DoesNotExist:
            messages.error(request, 'Error While Giving Wallet Balance For Quiz ')
            return redirect("admin_dashboard:quizanswers",user_id)


class UserGardeningProfileUpdateRequest(View):
    template = app + "garden_profile_update_request.html"
    model = models.GardeningProfileUpdateRequest

    def get(self, request):
        profile_update_obj = self.model.objects.all()
        request_prof_objs = []
        original_prof_objs = []
        for i in profile_update_obj:
            request_prof_objs.append(i)
            user = i.user
            original_profile_data = get_object_or_404(models.GardeningProfile,user = user)
            original_prof_objs.append(original_profile_data)
        print(request_prof_objs,original_prof_objs)
        data = zip(request_prof_objs,original_prof_objs)
        return render(request, self.template, locals())
    

def ApproveProfile(request, pk):
    prof_obj = get_object_or_404(models.GardeningProfileUpdateRequest, id=pk)
    if prof_obj is not None:
        user = prof_obj.user
        garden_area = prof_obj.garden_area
        number_of_plants = prof_obj.number_of_plants
        number_of_unique_plants = prof_obj.number_of_unique_plants
        garden_image = prof_obj.garden_image

        p_obj_for_update = get_object_or_404(models.GardeningProfile,user = user)

        p_obj_for_update.garden_area = garden_area
        p_obj_for_update.number_of_plants = number_of_plants
        p_obj_for_update.number_of_unique_plants = number_of_unique_plants
        p_obj_for_update.garden_image = garden_image
        
        send_template_email(
            subject="Gardening Profile Updated",
            template_name="mail_template/gardening_profile_approve_mail.html",
            context={'full_name': user.full_name,"email":user.email},
            recipient_list=[user.email]
        )

        # save the data to database and delete the update request object from db  
        p_obj_for_update.save()
        prof_obj.delete()
    else:
        msg = 'This account does not exist.'
        messages.error(request,msg)
    return redirect("admin_dashboard:gardeningprofileupdaterequest") 

def RejectProfile(request):
    if request.method == "POST":
        req_id = request.POST['user_id']
        reason = request.POST['reason']
        
        prof_obj = get_object_or_404(models.GardeningProfileUpdateRequest, id=int(req_id))
        if prof_obj is not None:
            user = prof_obj.user
            reject_object = models.GardeningProfileUpdateReject(user = user,gardening_profile_update_id = prof_obj.id,reason = reason)
            send_template_email(
                subject="Gardening Profile Rejected",
                template_name="mail_template/gardening_profile_rejected_mail.html",
                context={'full_name': user.full_name,"email":user.email},
                recipient_list=[user.email]
            )
            reject_object.save()
            prof_obj.delete()
        else:
            msg = 'This account does not exist.'
            messages.error(request,msg)
    return redirect("admin_dashboard:gardeningprofileupdaterequest") 


class UserActivityRequest(View):
    template = app + "activity_request.html"
    model = models.UserActivity

    def get(self, request):
        activity_request_obj = self.model.objects.filter(is_accepted='pending').order_by('-date_time')
        return render(request, self.template, locals())
    

def ApproveActivity(request, pk):
    req_obj = get_object_or_404(models.UserActivity,id = pk)
    if req_obj is not None:
        req_obj.is_accepted = "approved"
        user = get_object_or_404(models.User,id = req_obj.user.id)
        user.coins += 100
        send_template_email(
            subject="Activity Approved",
            template_name="mail_template/activity_approval_mail.html",
            context={'full_name': user.full_name,"email":user.email},
            recipient_list=[user.email]
        )
        user.save()
        req_obj.save()
        # Send email to the user that his/her request has been approved
    
        messages.info(request,"Activity Added successfully.")
    
    else:
        msg = 'This account does not exist.'
        messages.error(request,msg)

    return redirect("admin_dashboard:useractivityrequest") 

def RejectActivity(request):
    if request.method == "POST":
        req_id = request.POST['user_id']
        reason = request.POST['reason']
        
        req_obj = get_object_or_404(models.UserActivity,id = int(req_id))
        if req_obj is not None:
            req_obj.is_accepted = "rejected"
            req_obj.reject_reason = reason
            send_template_email(
                subject="Activity Rejected",
                template_name="mail_template/activity_rejection_mail.html",
                context={'full_name': req_obj.user.full_name,"email":req_obj.user.email,"reason":req_obj.reject_reason},
                recipient_list=[req_obj.user.email]
            )
            req_obj.save()
        else:
            msg = 'This account does not exist.'
            messages.error(request,msg)
    return redirect("admin_dashboard:useractivityrequest") 


class UserProduceSellRequest(View):
    template = app + "producesellrequest.html"
    model = models.SellProduce

    def get(self, request):
        sell_request_obj = self.model.objects.filter(is_approved='pending').order_by('-date_time')
        return render(request, self.template, locals())
    

def ApproveSellRequest(request):
    if request.method == "POST":
        sell_id = request.POST['sell_id']
        reason = request.POST['reason']

    sell_obj = get_object_or_404(models.SellProduce,id = int(sell_id))

    if sell_obj is not None:
        sell_obj.is_approved = "approved"
        sell_obj.reason = reason
        send_template_email(
            subject="Sell Request Approved",
            template_name="mail_template/sell_request_approve_mail.html",
            context={'full_name': sell_obj.user.full_name,"email":sell_obj.user.email,"reason":sell_obj.reason},
            recipient_list=[sell_obj.user.email]
        )
        sell_obj.save()
        
    else:
        msg = 'This account does not exist.'
        messages.error(request,msg)

    return redirect("admin_dashboard:sellrequest") 

def RejectSellRequest(request):
    if request.method == "POST":
        sell_id = request.POST['sell_id']
        reason = request.POST['reason']
        
        sell_obj = get_object_or_404(models.SellProduce,id = int(sell_id))
        if sell_obj is not None:
            sell_obj.is_approved = "rejected"
            sell_obj.reason = reason

            send_template_email(
                subject="Sell Request Rejected",
                template_name="mail_template/sell_request_reject_mail.html",
                context={'full_name': sell_obj.user.full_name,"email":sell_obj.user.email,"reason":sell_obj.reject_reason},
                recipient_list=[sell_obj.user.email]
            )
            
            sell_obj.save()
            
        else:
            msg = 'This account does not exist.'
            messages.error(request,msg)
    return redirect("admin_dashboard:sellrequest") 
