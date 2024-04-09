from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as app_commonmodels
from . import forms as user_form
from app_common import forms as common_forms
from django.shortcuts import get_object_or_404

from helpers import utils

app = "user_dashboard/"

#@method_decorator(utils.login_required, name='dispatch')
class UserDashboard(View):
    template = app + "index.html"

    def get(self, request):
        user = request.user
        users_orderby_coins = app_commonmodels.User.objects.filter(is_superuser=False).order_by('-coins')[:10]
        garden_obj = get_object_or_404(app_commonmodels.GardeningProfile, user=user)
        rank = user.get_rank()
        return render(request, self.template,locals())
    
class UserProfile(View):
    template = app + "user_profile.html"

    def get(self,request):
        return render(request,self.template)


class UpdateProfileView(View):
    template = app + "update_profile.html"
    form = user_form.UpdateProfileForm

    def get(self,request):
        user = request.user

        initial_data = {
        'full_name': user.full_name,
        'email': user.email,
        'contact': user.contact,
        'facebook_link':user.facebook_link,
        'instagram_link':user.instagram_link,
        'twitter_link':user.twitter_link,
        'youtube_link':user.youtube_link,
        'address':user.address,
        'user_image':user.user_image,
        'password': ''
        }

        form = self.form(initial=initial_data)

        data = {
            'form': form,
        }
        
        return render(request,self.template,data)
    
    def post(self,request):
       
        form = self.form(request.POST,request.FILES)

        if form.is_valid():
            user_obj = request.user

            email = form.cleaned_data['email']
            fullName = form.cleaned_data['full_name']
            contact = form.cleaned_data['contact']
            facebook_link = form.cleaned_data['facebook_link']
            instagram_link = form.cleaned_data['instagram_link']
            twitter_link = form.cleaned_data['twitter_link']
            youtube_link = form.cleaned_data['youtube_link']
            address = form.cleaned_data['address']
            user_image = form.cleaned_data['user_image']
            password = form.cleaned_data['password']

            try:
                user = app_commonmodels.User.objects.get(id=user_obj.id)
                user.email = email
                user.full_name = fullName
                user.contact = contact
                user.address = address
                user.facebook_link = facebook_link
                user.instagram_link = instagram_link
                user.twitter_link = twitter_link
                user.youtube_link = youtube_link

                if user_image is None:
                    picture = user.user_image
                else:
                    picture = user_image

                user.user_image = picture
            
                if password != '':
                    user.setPassword(password=password)
                
                user.save()
            
                messages.success(request,"Your profile has been updated successfully.")
                return redirect('user_dashboard:userprofile')
        
            except ValueError as e: 
                messages.error(request,e)  
        
        return render(request,self.template,locals())      

class ServicePage(View):
    template = app + "service.html"

    def get(self,request):
        return render(request,self.template)
    
class PrivacyPolicyPage(View):
    template = app + "privacypolicy.html"

    def get(self,request):
        return render(request,self.template)
    
class ContactePage(View):
    template = app + "contact.html"
    form = user_form.contactForm

    def get(self,request):
        data = {
            'form': self.form(),
        }
        return render(request,self.template,data)

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = request.user

            name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                contact_obj = app_commonmodels.User_Query(user = user,full_name = name,email = email,subject = subject,message = message)
                contact_obj.save()
                # msg = EmailMessage("Contact from %s"%name,message,to=[settings.EMAIL_HOST_USER])
                # msg.send()
                messages.success(request,'Query send Successfully. We will be in touch soon.')
                
            except Exception as e:
                print(str(e))
                messages.error(request,"Something went wrong!")
        else:
            messages.error(request,'Please correct the error below.') 
        
        return redirect('user_dashboard:contactpage')
    
class GardeningProfie(View):
    template = app + "gardening_profile.html"
    model = app_commonmodels.GardeningProfile

    def get(self,request):
        user = request.user
        try:
            garden_profile_obj = self.model.objects.get(user=user)
        except self.model.DoesNotExist:
            garden_profile_obj = None
        return render(request,self.template,locals())

import json
class UpdateGardeningProfileView(View):
    template = app + "edit_gardening_profile.html"
    form_class = common_forms.GardeningForm
    model = app_commonmodels.GardeningProfile

    def get(self,request):
        user = request.user
        try:
            user_obj = self.model.objects.get(user = user)
            form = self.form_class(instance=user_obj)
            context={'form':form}
        except self.model.DoesNotExist:
            messages.error(request,"No Data Found")
        
        return render(request, self.template, context)     

    def post(self,request):
        form = self.form_class(request.POST,request.FILES)
        user = request.user
        if form.is_valid():

            garden_area = form.cleaned_data['garden_area']
            number_of_plants = form.cleaned_data['number_of_plants']
            number_of_unique_plants = form.cleaned_data['number_of_unique_plants']
            garden_image = form.cleaned_data['garden_image']

            gardening_obj = self.model.objects.get(user=user)

            changes = []

            form_data = form.cleaned_data
            for field_name, value in form_data.items():
                if getattr(gardening_obj, field_name) != value:
                    changes.append(field_name)

            try:
                req_obj = app_commonmodels.GardeningProfileUpdateRequest.objects.filter(user=user)
                if len(req_obj)>0 :
                    #if there is already a pending update request then remove it  
                    req_obj[0].delete()
                gardening_obj = app_commonmodels.GardeningProfileUpdateRequest(user=user,garden_area = garden_area,number_of_plants = number_of_plants,number_of_unique_plants = number_of_unique_plants,garden_image = garden_image,changes = changes)              
                gardening_obj.save()
                messages.success(request,'Request Sent Successfully')
                return redirect('user_dashboard:gardeningprofile')
            except:
                messages.error(request,'Failed to Request data')
                return redirect('user_dashboard:gardeningprofileupdate')
        else:
            messages.error(request,'Please correct the below errors.')
            return redirect('user_dashboard:gardeningprofileupdate')
        

class AddActivityRequest(View):
    template = app + "activity_add.html"
    form_class = user_form.ActivityAddForm
    model = app_commonmodels.UserActivity

    def get(self,request):
        data = {
            'form': self.form_class(),
        }
        return render(request,self.template,data)
    
    def post(self,request):
        user = request.user
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid(): 
            activity_title = form.cleaned_data['activity_title']     
            activity_content = form.cleaned_data['activity_content']
            activity_image = form.cleaned_data['activity_image']
            # Save Activity 
            actvtyreqobj=self.model(user = user,activity_title = activity_title,activity_content = activity_content,activity_image = activity_image)
            actvtyreqobj.save()
            messages.success(request,'Request Sent Successfully')
            return redirect('user_dashboard:user_dashboard')
        else:
            messages.error(request,"Error! Please check your inputs.")
            return redirect('user_dashboard:addactivity')


class ActivityList(View):
    template = app + "activity_list.html"
    model = app_commonmodels.UserActivity

    def get(self,request):
        user = request.user
        activities = self.model.objects.filter(user = user,is_accepted = "approved").order_by('-date_time')
        data ={
                'activities' : activities,
             }
        return render(request,self.template,data)


class WalletView(View):
    template = app + "wallet.html"
    model = app_commonmodels.Wallet_Trasnsaction_History

    def get(self,request):
        user = request.user
        try:
            transactions = self.model.objects.get(user=user)
            dict_transaction = transactions.history
        except Exception:
            dict_transaction = None
        return render(request,self.template,locals())
    


class SellProduceView(View):
    template = app + "sell_produce.html"
    form_class = user_form.SellProduceForm
    model = app_commonmodels.SellProduce

    def get(self,request):
        data = {
            'form': self.form_class(),
        }
        return render(request,self.template,data)
    
    def post(self,request):
        user = request.user
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid(): 
            product_name = form.cleaned_data['product_name'] 
            product_image = form.cleaned_data['product_image']    
            product_quantity = form.cleaned_data['product_quantity']
            SI_units = form.cleaned_data['SI_units']
            ammount_in_green_points = form.cleaned_data['ammount_in_green_points']

            # Save SellProduce
            
            sellObj=self.model(user = user,product_name = product_name,product_image = product_image,product_quantity = product_quantity,SI_units = SI_units,ammount_in_green_points = ammount_in_green_points)
            sellObj.save()
            messages.success(request,'Request for sell Sent Successfully')
            return redirect('user_dashboard:user_dashboard')
        else:
            messages.error(request,"Error! Please check your inputs.")
            return redirect('user_dashboard:addactivity')

class AllSellRequests(View):
    template = app + "sellrequestlist.html"
    model = app_commonmodels.SellProduce
    def get(self,request):
        user = request.user
        sell_objs = self.model.objects.filter(user=user).order_by("-id")
        return render(request,self.template,locals())
    
class GreenCommerceProductCommunity(View):
    template = app + "greencommerceproducts.html"
    model = app_commonmodels.SellProduce

    def get(self,request):
        produce_obj = self.model.objects.filter(is_approved = "approved").order_by("-date_time")
        context={'produces':produce_obj}
        return render(request,self.template,context)

from datetime import datetime  
class ProduceBuyView(View):
    model = app_commonmodels.SellProduce
    def get(self,request,prod_id):
        user = request.user
        buyer = app_commonmodels.User.objects.get(id = user.id)
        sell_prod_obj = self.model.objects.get(id=prod_id)
        seller = sell_prod_obj.user
        product_quantity = sell_prod_obj.product_quantity
        SI_units = sell_prod_obj.SI_units
        ammount_in_green_points = sell_prod_obj.ammount_in_green_points

        try:
            if buyer.wallet >= ammount_in_green_points:
                buying_obj = app_commonmodels.ProduceBuy(buyer = buyer,seller = seller,sell_produce = sell_prod_obj.product_name,product_quantity = product_quantity,SI_units = SI_units,ammount_in_green_points = ammount_in_green_points)
                buyer.wallet -= ammount_in_green_points
                buyer.total_invest += ammount_in_green_points
                buyer.coins += 50
                
                seller.wallet += ammount_in_green_points
                seller.total_income += ammount_in_green_points
                seller.coins += 50

                current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                transaction_user_buyer, created = app_commonmodels.Wallet_Trasnsaction_History.objects.get_or_create(user = user)
                json_data = transaction_user_buyer.history or {}
                two_values = {'amount': "-"+str(ammount_in_green_points), 'date_time': current_date_time}
                json_data[sell_prod_obj.product_name] = two_values
                transaction_user_buyer.history = json_data
                transaction_user_buyer.save()

                transaction_user_seller, created = app_commonmodels.Wallet_Trasnsaction_History.objects.get_or_create(user = seller)
                json_data = transaction_user_seller.history or {}
                two_values = {'amount': "+"+str(ammount_in_green_points), 'date_time': current_date_time}
                json_data[sell_prod_obj.product_name] = two_values
                transaction_user_seller.history = json_data
                transaction_user_seller.save()

                buying_obj.save()
                buyer.save()
                seller.save()
                sell_prod_obj.delete()
                return redirect('user_dashboard:greencommerceproducts')  
            else:
                messages.error(request,"You don't have enough green points in your wallet!")
                return redirect('user_dashboard:greencommerceproducts')
        except Exception as e:
            print(e)
            return redirect('user_dashboard:greencommerceproducts')

