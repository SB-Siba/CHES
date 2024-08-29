from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as app_commonmodels
from . import forms as user_form
from app_common import forms as common_forms
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from helpers import utils
from chatapp.models import Message
from . serializers import DirectBuySerializer,OrderSerializer
import ast
import datetime
from serviceprovider.forms import BookingForm,ReviewForm
from EmailIntigration.views import send_template_email
from django.db.models.functions import Lower

app = "user_dashboard/"

class UserDashboard(View):
    template = app + "index.html"

    def get(self, request):
        user = request.user
        # Deleting Expire Produce
        try:
            sell_produce_obj  = app_commonmodels.SellProduce.objects.all()
            for i in sell_produce_obj:
                if i.days_left_to_expire <= 0:
                    i.delete()
        except Exception:
            pass
        users_orderby_coins = app_commonmodels.User.objects.filter(is_superuser=False,is_rtg = True).order_by('-coins')[:5]
        users_name = [u.full_name for u in users_orderby_coins]
        user_coins = [u_coin.coins for u_coin in users_orderby_coins]
        garden_obj = app_commonmodels.GardeningProfile.objects.filter(user = user).first()
        rank = user.get_rank("rtg")
        print(users_name,user_coins)
        context = {
            'user':user,
            'users_orderby_coins':users_orderby_coins,
            'users_name':users_name,
            'u_coins':user_coins,
            'garden_obj':garden_obj,
            'rank' : rank,
        }
        return render(request, self.template,context)
    
class UserProfile(View):
    template = app + "user_profile.html"

    def get(self,request):
        rating_of_user = request.user.calculate_avg_rating()
        return render(request,self.template,locals())


class UpdateProfileView(View):
    template = app + "update_profile.html"
    form = user_form.UpdateProfileForm

    def get(self,request):
        print("lklk")
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
    
class GardeningProfile(View):
    template = app + "gardening_profile.html"
    model = app_commonmodels.GardeningProfile

    def get(self,request):
        user = request.user
        try:
            garden_profile_obj = self.model.objects.get(user=user)
            garden_area = garden_profile_obj.garden_area
            # Assume each tree needs 4 square ft and each pot needs 1 square ft
            trees = garden_area // 4
            pots = garden_area // 1
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
    model = app_commonmodels.ProduceBuy

    def get(self,request):
        user = request.user
        try:
            transactions = self.model.objects.filter((Q(buyer=user) | Q(seller=user)) & Q(buying_status="PaymentDone") | Q(buying_status="BuyCompleted")).order_by('-date_time')
            list_of_transactions = []
            xyz = []
            for i in transactions:
                list_of_transactions.append(i)
                if i.buyer == user:
                    x = True
                    xyz.append(x)
                else:
                    x = False
                    xyz.append(x)
            main_obj = zip(list_of_transactions,xyz)  
            
        except Exception:
            transactions = None
            
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
            validity_duration_days = form.cleaned_data['validity_duration_days']

            # Save SellProduce
            
            sellObj=self.model(user = user,product_name = product_name,product_image = product_image,product_quantity = product_quantity,SI_units = SI_units,ammount_in_green_points = ammount_in_green_points,validity_duration_days = validity_duration_days)
            sellObj.save()
            messages.success(request,'Request for sell Sent Successfully')
            return redirect('user_dashboard:user_dashboard')
        else:
            messages.error(request,"Error! Please check your inputs.")
            return redirect('user_dashboard:sellproduce')


def delete_expired_sell_produce(request):
    """
    This function is used to delete the expired sell produce from database.
    It will be called in every midnight by a cron job.
    0 0 * * * /path/to/python /path/to/your/manage.py shell -c "from yourapp.utils import delete_expired_sell_produce; delete_expired_sell_produce()"
    """
    current_date = timezone.now()
    app_commonmodels.SellProduce.objects.filter(validity__lte=current_date).delete()
   




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
    form = user_form.BuyQuantityForm

    def get(self,request):
        produce_obj = self.model.objects.exclude(user=request.user).filter(is_approved="approved").order_by("-date_time")
        ratings_list = [i.user.calculate_avg_rating() for i in produce_obj]
        message_status = []
        for i in produce_obj:
            msg_obj = Message.objects.filter(Q(receiver=i.user,sender=request.user) | Q(receiver=request.user,sender=i.user))
            if msg_obj:
                message_status.append(True)
            else:
                message_status.append(False)
       
        zipped_value = zip(produce_obj,message_status,ratings_list)
        context={'zipped_value':zipped_value,'form':self.form}
        return render(request,self.template,context)


class BuyingBegins(View):
    model = app_commonmodels.SellProduce
    
    def post(self,request,prod_id):
        user = request.user
        try:
            buyer = app_commonmodels.User.objects.get(id = user.id)
            sell_prod_obj = self.model.objects.get(id=prod_id)
            seller = sell_prod_obj.user
            product_quantity = sell_prod_obj.product_quantity
            SI_units = sell_prod_obj.SI_units
            ammount_in_green_points = sell_prod_obj.ammount_in_green_points

            form_data = request.POST
            quantity = int(form_data['quantity'])
            
            # print(type(prod_id),type(quantity))
            if product_quantity >= quantity:
                try:
                    if buyer.wallet >= ammount_in_green_points:
                        buying_obj = app_commonmodels.ProduceBuy(buyer = buyer,seller = seller,sell_produce = sell_prod_obj,product_name = sell_prod_obj.product_name,SI_units = SI_units,buying_status = 'BuyInProgress',quantity_buyer_want = quantity)
                        buying_obj.save()
                        return redirect('user_dashboard:user_dashboard')
                    else:
                        messages.error(request,"You don't have enough green points in your wallet!")
                        return redirect('user_dashboard:greencommerceproducts')
                except Exception as e:
                    print(e)
                    return redirect('user_dashboard:greencommerceproducts')
            else:
                messages.error(request,"The requested amount is not available.")
                return redirect('user_dashboard:greencommerceproducts') 
        except self.model.DoesNotExist:
            messages.error(request,"The product is not available.")
            return redirect('user_dashboard:greencommerceproducts')



class BuyBeginsSellerView(View):
    template = app + "buyingprogressseller.html"
    model = app_commonmodels.ProduceBuy
    form = user_form.BuyAmmountForm
    def get(self,request):
        user = request.user
        bbeigins_obj = self.model.objects.filter(seller=user, buying_status="BuyInProgress")
        form = self.form
        return render(request,self.template,locals())
    
class BuyBeginsBuyerView(View):
    template = app + "buyingprogressbuyer.html"
    model = app_commonmodels.ProduceBuy
    def get(self,request):
        user = request.user
        bbeigins_obj = self.model.objects.filter(buyer=user, buying_status="BuyInProgress")
        
        return render(request,self.template,locals())
    
def send_payment_link(request,buy_id):
    if request.method == "POST":
        buy_obj = app_commonmodels.ProduceBuy.objects.get(id=buy_id)
        form_data = request.POST
        ammount_based_on_buyer_quantity = int(form_data['ammount_based_on_buyer_quantity'])
        buy_obj.payment_link = "Send"
        buy_obj.ammount_based_on_quantity_buyer_want = ammount_based_on_buyer_quantity
        buy_obj.save()

        return redirect('user_dashboard:buybeginssellerview')


class ProduceBuyView(View):
    model = app_commonmodels.ProduceBuy
    def get(self,request,ord_id):
        user = request.user
        buy_prod_obj = self.model.objects.get(id=ord_id)
        seller = buy_prod_obj.seller
        buyer = buy_prod_obj.buyer
        ammount_for_quantity_want = buy_prod_obj.ammount_based_on_quantity_buyer_want
        sell_prod = buy_prod_obj.sell_produce


        try:
            buyer.wallet -= ammount_for_quantity_want
            buyer.total_invest += ammount_for_quantity_want
            buyer.coins += 50
                
            seller.wallet += ammount_for_quantity_want
            seller.total_income += ammount_for_quantity_want
            seller.coins += 50

            sell_prod_obj = app_commonmodels.SellProduce.objects.get(id = sell_prod.id)
            sell_prod_obj.product_quantity = sell_prod_obj.product_quantity-buy_prod_obj.quantity_buyer_want
            sell_prod_obj.ammount_in_green_points = sell_prod_obj.ammount_in_green_points - ammount_for_quantity_want
            buy_prod_obj.buying_status = "BuyCompleted"
            buy_prod_obj.save()
            sell_prod_obj.save()
            buyer.save()
            seller.save()
            return redirect('user_dashboard:greencommerceproducts')  

        except Exception as e:
            print(e)
            return redirect('user_dashboard:greencommerceproducts')


def reject_buy(request,ord_id):
    order_obj = app_commonmodels.ProduceBuy.objects.get(id=ord_id)
    order_obj.buying_status="BuyRejected"
    order_obj.save()
    return redirect('user_dashboard:buybeginssellerview')

    

class AllOrders(View):
    template = app + "all_orders.html"
    model = app_commonmodels.ProduceBuy

    def get(self, request):
        orders = self.model.objects.filter(buyer=request.user)
        return render(request , self.template , {'orders' : orders})
    
class AllPosts(View):
    template = app + "all_posts.html"
    model = app_commonmodels.UserActivity
    def get(self,request):
        posts = self.model.objects.filter(is_accepted = "approved").order_by("-id")
        posts_list = []
        like_list = []
        like_count_per_activity = []
        comment_count_per_activity = []

        for i in posts:
            if request.user.full_name in i.likes: 
                posts_list.append(i)     
                like_count_per_activity.append(len(i.likes))  
                comment_count_per_activity.append(len(i.comments))
                like_list.append(1)
            else:
                posts_list.append(i)
                like_count_per_activity.append(len(i.likes))
                comment_count_per_activity.append(len(i.comments))
                like_list.append(0)
        
        # print(posts_list,"\n",like_list,"\n",like_count_per_activity,"\n",comment_count_per_activity)
        post_and_like = zip(posts_list,like_list,like_count_per_activity,comment_count_per_activity)
        return render(request , self.template ,locals())
    

def plus_like(request):
    if request.method == 'GET':
        user = request.user
        actvity_id = request.GET['activity_id']
        activity_obj = app_commonmodels.UserActivity.objects.get(id = int(actvity_id))
        if user.full_name not in activity_obj.likes:
            activity_obj.likes.append(user.full_name)
        activity_obj.save()
        data={'status':'Product added to wishlist'}
        return JsonResponse(data)
    
def minus_like(request):
    if request.method == 'GET':
        user = request.user
        actvity_id = request.GET['activity_id']
        activity_obj = app_commonmodels.UserActivity.objects.get(id = int(actvity_id))
        if user.full_name in activity_obj.likes:
            activity_obj.likes.remove(user.full_name)
        activity_obj.save()
        data={'status':'Product removed from wishlist'}
        return JsonResponse(data)
    
def give_comment(request):
    if request.method == "POST":
        commenter=request.user.full_name
        comment=request.POST["comment"]
        post=request.POST["post"]
        post_obj = app_commonmodels.UserActivity.objects.get(id = int(post)) 
    
        comment_data = {
            "id": str(datetime.datetime.now().timestamp()),  # unique ID for the comment
            "commenter": commenter,
            "comment": comment
        }
        post_obj.comments.append(comment_data)
        post_obj.save()
        return redirect('user_dashboard:allposts')
    
def delete_comment(request, post_id, comment_id):    
    post_obj = app_commonmodels.UserActivity.objects.get(id=post_id)
        
    # Find the comment by its ID
    post_obj.comments = [comment for comment in post_obj.comments if comment["id"] != comment_id]
        
    post_obj.save()
    return redirect('user_dashboard:allposts')
    
def get_all_comments(request):
    post_id = request.GET.get('post_id')
    activity_obj = app_commonmodels.UserActivity.objects.filter(id=int(post_id)).first()
    current_user = request.user.full_name
    
    if activity_obj:
        comments_data = activity_obj.comments  # Assuming comments_data is a list of dictionaries
        response_data = {
            'current_user': current_user,
            'comments': comments_data
        }
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'current_user': current_user, 'comments': []}, safe=False)

class RateOrder(View):
    model = app_commonmodels.ProduceBuy

    def post(self,request):
        order_id = request.POST.get("order_id")
        rating = request.POST.get("rating")
        # print(order_id,rating)
        buy_obj = get_object_or_404(self.model,id = order_id)
        seller = buy_obj.seller
        buyer = buy_obj.buyer
        if seller.ratings is None:
            seller.ratings = []

        new_rating = {
            "buyer_name": buyer.full_name,
            "order_product": buy_obj.product_name,
            "quantity": buy_obj.quantity_buyer_want,
            "ammount_paid": buy_obj.ammount_based_on_quantity_buyer_want,
            "rating": rating,
        }
        seller.ratings.append(new_rating)
        buy_obj.rating_given = True
        buy_obj.save()
        seller.save()
        return redirect('user_dashboard:allorders')
    
class VendorsProduct(View):
    template = app + "vendor_products.html"
    model = app_commonmodels.ProductFromVendor

    def get(self,request):
        products = self.model.objects.all().order_by("-id")
        ratings_list = [i.calculate_avg_rating() for i in products]
        message_status = []
        for i in products:
            msg_obj = Message.objects.filter(Q(receiver=i.vendor,sender=request.user) | Q(receiver=request.user,sender=i.vendor))
            if msg_obj:
                message_status.append(True)
            else:
                message_status.append(False)
       
        zipped_value = zip(products,message_status,ratings_list)
        context={'zipped_value':zipped_value}
        return render(request,self.template,context)
    
class CheckoutView(View):
    template = app + "checkout_page.html"
    form = user_form.CheckoutForm

    def get(self,request,vprod_id,vendor_email):
        user = request.user
        offer_discount = request.GET.get('offer_discount', None)
        
        initial_data = {
        'username': user.email,
        }

        form = self.form(initial=initial_data)
        vendor_product_obj = get_object_or_404(app_commonmodels.ProductFromVendor,id = vprod_id)
        serializer = DirectBuySerializer(vendor_product_obj,context={'offer_discount': offer_discount})
        order_details = serializer.data
        # print(order_details)
        ord_meta_data = {}
        for i,j in order_details.items():
            ord_meta_data.update(j)

        discount_amount = float(ord_meta_data['discount_amount'])
        discount_amount = '{:.2f}'.format(discount_amount)
        delivery_charge = ord_meta_data['charges']["Delivery"]
        # Using round() function for discount_percentage, t_price, and our_price
 
        discount_percentage = ord_meta_data['discount_percentage']
        t_price = ord_meta_data['final_value']
        our_price = ord_meta_data['our_price']
        gross_ammount = ord_meta_data['gross_value']
        # print(ord_meta_data)
        data = {
            'form': form,
            "vendor_product":vendor_product_obj,
            "gross_ammount":gross_ammount,
            "our_price":our_price,
            "discount_ammount":discount_amount,
            "discount_percentage":discount_percentage,
            "total":t_price,
            "offer_discount":offer_discount,
            'delivery_charge':delivery_charge
            }
        return render(request, self.template, data)
    def post(self,request,vprod_id,vendor_email):
        form = self.form(request.POST)
        offer_discount = request.POST.get('offer_discount', None)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name']    
            username = form.cleaned_data['username']
            contact_number = form.cleaned_data['contact_number']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            zip_code = form.cleaned_data['zip_code']
            same_address = form.cleaned_data['same_address']
            save_info = form.cleaned_data['save_info']

            customer_details = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'contact_number':contact_number,
                'email': email,
                'address': address,
                'city': city,
                'zip_code': zip_code,
            }

            prod_obj = get_object_or_404(app_commonmodels.ProductFromVendor,id = vprod_id)
            
            serializer = DirectBuySerializer(prod_obj,context={'offer_discount': offer_discount})
            order_details = serializer.data
            # print(order_details)
            ord_meta_data = {}
            for i,j in order_details.items():
                ord_meta_data.update(j)
                
            t_price = ord_meta_data['final_value']

            try:
                vendor = get_object_or_404(app_commonmodels.User,email = vendor_email)
                
                order = app_commonmodels.Order(
                    customer = user,
                    vendor = vendor,
                    products={prod_obj.name:1},
                    order_value=t_price,
                    customer_details=customer_details,
                    order_meta_data = ord_meta_data
                    # razorpay_payment_id = razorpay_payment_id,
                    # razorpay_order_id= razorpay_order_id,
                    # razorpay_signature= razorpay_signature,
                )
                # order.order_meta_data = json.loads(ord_meta_data)
         
                if int(offer_discount) == 1:
                    user.wallet -= float(prod_obj.green_coins_required)
                    vendor.wallet += float(prod_obj.green_coins_required)
                    user.save()
                    vendor.save()
            
                order.save()
                prod_obj.stock -= 1
                prod_obj.save()

                send_template_email(
                    subject="Order Successfull",
                    template_name="mail_template/successfull_order_mail.html",
                    context={'full_name': user.full_name,"email":user.email,"order_number":order.uid,"order_date":order.date,"order_total":t_price},
                    recipient_list=[user.email]
                )

                return redirect("user_dashboard:user_dashboard")
            except Exception as e:
                print(e)
                messages.error(request, "Error while placing Order.")
                return redirect("user_dashboard:user_dashboard")
            
        initial_data = {
        'username': request.user.email,
        }

        form = self.form(initial=initial_data)
        vendor_product_obj = get_object_or_404(app_commonmodels.ProductFromVendor,id = vprod_id)
        serializer = DirectBuySerializer(vendor_product_obj,context={'offer_discount': offer_discount})
        order_details = serializer.data
        # print(order_details)
        ord_meta_data = {}
        for i,j in order_details.items():
            ord_meta_data.update(j)

        discount_amount = ord_meta_data['discount_amount']
        gst = ord_meta_data['charges']["GST"]
        delivery_charge = float(ord_meta_data['charges']["Delivary"])
        discount_percentage = ord_meta_data['discount_percentage']
        t_price = ord_meta_data['final_value']
        our_price = ord_meta_data['our_price']
        gross_ammount = ord_meta_data['gross_value']
        data = {
            'form': form,
            "vendor_product":vendor_product_obj,
            "gross_ammount":gross_ammount,
            "our_price":our_price,
            "discount_ammount":discount_amount,
            "discount_percentage":discount_percentage,
            "gst":gst,
            "total":t_price,
            "offer_discount":offer_discount,
            'delivery_charge':delivery_charge
            }
        return render(request, self.template, data)
    
class AllOrdersFromVendors(View):
    model = app_commonmodels.Order
    template = app + "all_orders_from_vendor.html"

    def get(self,request):
        user = request.user
        orders = self.model.objects.filter(customer=request.user).order_by("-id")
        order_list = []
        products_list = []
        for order in orders:
            order_products = []
            order_items = order.products
            for name, quantity in order_items.items():
                order_products.append(get_object_or_404(app_commonmodels.ProductFromVendor,name = name))
            
            products_list.append(order_products)
            order_list.append(order)
        print(order_list)
        order_and_products = zip(order_list, products_list)
        
        context={'order_and_products':order_and_products}
        return render(request,self.template,context)
    
class GardenerDownloadInvoice(View):
    model = app_commonmodels.Order
    template = app + "invoice.html"

    def get(self,request, order_uid):
        order = self.model.objects.get(uid = order_uid)
        data = OrderSerializer(order).data
        product = ""
        quantity = 0
        price_per_unit = 0
        total_price = 0
        our_price = 0
        cgst = 0
        sgst = 0
        taxable_price = 0
        coin_exchange = data['order_meta_data']['coin_exchange']
        coins_for_exchange = 0
        exchange_percentage = 0
        
        for product,p_overview in data['order_meta_data']['products'].items():
            product = product
            quantity = p_overview['quantity']
            price_per_unit = p_overview['price_per_unit']
            total_price = p_overview['total_price']
            our_price = p_overview['our_price']
            cgst = p_overview['cgst']
            sgst = p_overview['sgst']
            taxable_price = p_overview['taxable_price']
            if coin_exchange:
                coins_for_exchange = p_overview['coinexchange']
                exchange_percentage = p_overview['forpercentage']      
        
        context ={
            'order':data,
            'details':data['customer_details'],
            'customer':order.customer,
            'vendor':order.vendor,
            'product':product,
            'quantity':quantity,
            'price_per_unit':price_per_unit,
            'total_price':total_price,
            "our_price":our_price,
            'cgst':cgst,
            'sgst':sgst,
            'taxable_price':taxable_price,
            'delevery_charge':data['order_meta_data']['charges']['Delivery'],
            'gross_amt':data['order_meta_data']['our_price'],
            'discount':data['order_meta_data']['discount_amount'],
            'final_total':data['order_meta_data']['final_value'],
            'coin_exchange':coin_exchange,
            'coins_for_exchange':coins_for_exchange,
            'exchange_percentage':exchange_percentage
        }
        
        return render(request,self.template,context)
    
class ServiceProvidersList(View):
    model = app_commonmodels.ServiceProviderDetails
    template = app + "service_providers_list.html"

    def get(self,request):
        service_providers = self.model.objects.filter(provider__is_approved = True)
        providers = []
        areas = []
        types = []
        for i in service_providers:
            service_types = ast.literal_eval(i.service_type)
            service_areas = ast.literal_eval(i.service_area)
            providers.append(i)
            types.append(service_types)
            areas.append(service_areas)

        providers_area_types = zip(providers,areas,types)
        context = {'providers_area_types':providers_area_types}
        return render(request,self.template,context)
    

class ListOfServicesByServiceProviders(View):
    template = app + "list_services.html"
    model = app_commonmodels.Service

    def get(self, request):
        services = self.model.objects.all()
        return render(request , self.template , {'services' : services})

class ServiceSearchView(View):
    model = app_commonmodels.Service
    template = app + "list_services.html"

    def get(self, request):
        search_query = request.GET.get('search_query')

        if search_query:
            # Convert the search query to lowercase
            search_query_lower = search_query.lower()

            # Filter services by converting both the name and service_type to lowercase
            services = app_commonmodels.Service.objects.annotate(
                name_lower=Lower('name'),
                service_type_lower=Lower('service_type')
            ).filter(
                Q(name_lower__icontains=search_query_lower) | Q(service_type_lower__icontains=search_query_lower)
            )
        else:
            services = app_commonmodels.Service.objects.all()

        context = {
            'services': services,
        }
        return render(request, self.template, context)

class ServiceDetails(View):
    template = app + "service_details.html"
    model = app_commonmodels.Service
    form_class = BookingForm
    def get(self,request, service_id):
        form = BookingForm()
        service = get_object_or_404(self.model, id=service_id)
        service_booked_obj = app_commonmodels.Booking.objects.filter(service = service,gardener = request.user,status = "pending")
        return render(request, self.template, {'service': service,"form":form,"service_booked_obj":service_booked_obj})
    def post(self,request, service_id):
        form = BookingForm(request.POST)
        service = get_object_or_404(self.model, id=service_id)
        service_booked_obj = app_commonmodels.Booking.objects.filter(service = service,gardener = request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.gardener = request.user
            booking.save()
            return redirect("user_dashboard:list_services")
        return render(request, self.template, {'service': service,"form":form,"service_booked_obj":service_booked_obj})
    
class MyBookedServices(View):
    template = app + "my_booked_services.html"
    model = app_commonmodels.Booking
    def get(self,request):
        booked_services = self.model.objects.filter(gardener=request.user).exclude(status="declined")
        # booked_services = self.model.objects.filter(gardener = request.user)
        return render(request, self.template, {'booked_services': booked_services})

def rtg_decline_booking(request, booking_id):
    booking = get_object_or_404(app_commonmodels.Booking, id=booking_id)
    if request.user == booking.gardener:
        booking.status = 'declined'
        booking.save()
    return redirect('user_dashboard:my_booked_services')

class RateOrderFromVendor(View):
    model = app_commonmodels.Order

    def post(self,request):
        order_id = request.POST.get("order_id")
        rating = request.POST.get("rating")
        # print(order_id,rating)
        buy_obj = get_object_or_404(self.model,id = order_id)
        vendor = buy_obj.vendor
        customer = buy_obj.customer
        product = ""
        print(buy_obj.products,type(buy_obj.products))
        for i,j in buy_obj.products.items():
            product = i
        product_obj = get_object_or_404(app_commonmodels.ProductFromVendor,name = product)     
        if product_obj.ratings is None:
            product_obj.ratings = []

        new_rating = {
            "buyer_name": customer.full_name,
            "order_product": product,
            "ammount_paid": float(buy_obj.order_value),
            "rating": rating,
        }
        product_obj.ratings.append(new_rating)
        buy_obj.rating_given = True
        buy_obj.rating = rating
        buy_obj.save()
        product_obj.save()
        return redirect('user_dashboard:allordersfromvendor')