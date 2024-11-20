import datetime
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as common_models
from EmailIntigration.views import send_template_email
from user_dashboard.serializers import OrderSerializer
from user_dashboard.forms import ActivityAddForm, BuyAmmountForm,SellProduceForm,BuyQuantityForm
from app_common.forms import GardeningForm, VendorQRForm
from . import forms as common_forms
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from helpers import utils
from chatapp.models import Message
from admin_dashboard.orders.forms import OrderUpdateForm
from django.utils.timezone import now
from django.db.models.functions import Lower
import ast
from serviceprovider.forms import BookingForm
from app_common.error import render_error_page
from app_common.forms import contactForm
from django.utils.decorators import method_decorator
from helpers import utils
from helpers.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from datetime import datetime, date, time
from django.utils import timezone


app = "vendor_dashboard/"

@method_decorator(utils.login_required, name='dispatch')
class VendorDashboard(View):
    template = app + "home.html"

    def get(self, request):
        try:
            user = request.user 
            vendors = common_models.User.objects.filter(is_vendor=True)[:10]
            valid_order_statuses = ["Placed", "Accepted", "On_Way", "Delivered"]

            def calculate_earnings(vendor, start_date, end_date):
                orders = common_models.Order.objects.filter(
                    vendor=vendor, 
                    date__range=(start_date, end_date),
                    order_status__in=valid_order_statuses
                )
                return sum(order.order_value for order in orders)

            today = now().date()
            start_of_month = today.replace(day=1)
            start_of_year = today.replace(month=1, day=1)
            start_of_day = now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now().replace(hour=23, minute=59, second=59, microsecond=999999)

            vendor_and_sellamounts_today = [(vendor, calculate_earnings(vendor, start_of_day, end_of_day)) for vendor in vendors]
            vendor_and_sellamounts_month = [(vendor, calculate_earnings(vendor, start_of_month, today)) for vendor in vendors]
            vendor_and_sellamounts_year = [(vendor, calculate_earnings(vendor, start_of_year, today)) for vendor in vendors]

            vendor_and_sellamounts_today.sort(key=lambda x: x[1], reverse=True)
            vendor_and_sellamounts_month.sort(key=lambda x: x[1], reverse=True)
            vendor_and_sellamounts_year.sort(key=lambda x: x[1], reverse=True)

            max_earnings_today = max(vendor_and_sellamounts_today, key=lambda x: x[1])[1] if vendor_and_sellamounts_today else 0
            max_earnings_month = max(vendor_and_sellamounts_month, key=lambda x: x[1])[1] if vendor_and_sellamounts_month else 0
            max_earnings_year = max(vendor_and_sellamounts_year, key=lambda x: x[1])[1] if vendor_and_sellamounts_year else 0

            vendor_and_percentages_today = [(vendor, amount, (amount / max_earnings_today * 100) if max_earnings_today else 0) for vendor, amount in vendor_and_sellamounts_today]
            vendor_and_percentages_month = [(vendor, amount, (amount / max_earnings_month * 100) if max_earnings_month else 0) for vendor, amount in vendor_and_sellamounts_month]
            vendor_and_percentages_year = [(vendor, amount, (amount / max_earnings_year * 100) if max_earnings_year else 0) for vendor, amount in vendor_and_sellamounts_year]


            earnings_today = calculate_earnings(user, start_of_day, end_of_day)
            earnings_month = calculate_earnings(user, start_of_month, today)
            earnings_year = calculate_earnings(user, start_of_year, today)

            users_orderby_coins = common_models.User.objects.filter(
                Q(is_vendor=True),
                is_approved=True,
                is_superuser=False
            ).order_by('-coins')[:10]
            users_name = [u.full_name for u in users_orderby_coins]
            user_coins = [u_coin.coins for u_coin in users_orderby_coins]
            print(users_name,user_coins)

            context = {
                'vendor_and_percentages_today': vendor_and_percentages_today,
                'vendor_and_percentages_month': vendor_and_percentages_month,
                'vendor_and_percentages_year': vendor_and_percentages_year,
                'max_earnings_today': max_earnings_today,
                'max_earnings_month': max_earnings_month,
                'max_earnings_year': max_earnings_year,

                'earnings_today': earnings_today,
                'earnings_month': earnings_month,
                'earnings_year': earnings_year,

                'users_orderby_coins':users_orderby_coins,
                'users_name':users_name,
                'u_coins':user_coins,
            }
            return render(request, self.template,context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class VendorProfile(View):
    template = app + "vendor_profile.html"

    def get(self, request):
        try:
            user = request.user 
            vendor_obj = get_object_or_404(common_models.VendorDetails,vendor = user)
            return render(request, self.template, {'vendor_obj':vendor_obj})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class UpdateProfileView(View):
    template_name = app+"vendor_update_profile.html"
    form_class = common_forms.VendorDetailsForm
    model = common_models.VendorDetails
    
    def get(self, request):
        try:
            vendor_details = get_object_or_404(self.model, vendor=request.user)
            initial_data = {
                'business_name': vendor_details.business_name,
                'business_address': vendor_details.business_address,
                'business_description': vendor_details.business_description,
                'business_license_number': vendor_details.business_license_number,
                'establishment_year': vendor_details.establishment_year,
                'website': vendor_details.website,
                'established_by': vendor_details.established_by,
            }

            # If the category is not in the predefined options, use it as a custom category
            if vendor_details.business_category not in dict(self.form_class.BUSINESS_CATEGORIES):
                initial_data['custom_business_category'] = vendor_details.business_category
                initial_data['business_category'] = 'other'
            # print(initial_data,"llll")
            form = self.form_class(initial=initial_data)
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    
    def post(self, request):
        try:
            vendor_details = get_object_or_404(self.model, vendor=request.user)
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():
                business_name = form.cleaned_data['business_name']
                business_address = form.cleaned_data['business_address']
                business_description = form.cleaned_data['business_description']
                business_license_number = form.cleaned_data['business_license_number']
                establishment_year = form.cleaned_data['establishment_year']
                website = form.cleaned_data['website']
                established_by = form.cleaned_data['established_by']

                # Extract the business category and check if 'Other' is selected
                business_category = form.cleaned_data['business_category']
                custom_business_category = form.cleaned_data.get('custom_business_category', '')

                # If 'Other' is selected, use the custom business category
                if business_category == 'other' and custom_business_category:
                    business_category = custom_business_category

                if 'image' in request.FILES:
                    image = request.FILES['image']
                else:
                    if vendor_details.vendor.user_image:
                        image = vendor_details.vendor.user_image
                    else:
                        image = None
                print(image)
                vendor_details.business_name = business_name
                vendor_details.business_address = business_address
                vendor_details.business_category = business_category
                vendor_details.business_description = business_description
                vendor_details.business_license_number = business_license_number
                vendor_details.established_by = established_by
                vendor_details.establishment_year = establishment_year
                vendor_details.website = website
            
                    
                user_obj = get_object_or_404(common_models.User,id = vendor_details.vendor.id)
                user_obj.user_image = image
                user_obj.save()
                vendor_details.save()

                return redirect('vendor_dashboard:vendor_profile')
            else:
                error_message = f"Please correct your inputs"
                return render_error_page(request, error_message, status_code=400)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class VendorSellProduct(View):
    template = app + "vendor_sell_product.html"
    form_class = common_forms.ProductFromVendorForm
    model = common_models.ProductFromVendor

    def get(self,request):
        # try:
            data = {
                'form': self.form_class(),
            }
            return render(request,self.template,data)
        # except Exception as e:
        #     error_message = f"An unexpected error occurred: {str(e)}"
        #     return render_error_page(request, error_message, status_code=400)
    
    def post(self,request):
        # try:
            user = request.user
            form = self.form_class(request.POST,request.FILES)
            if form.is_valid(): 
                product = form.save(commit=False)  # Don't save the form yet
                product.vendor = user  # Set the vendor to the current logged-in user
                # Handle the custom category if "Other" is selected
                category = form.cleaned_data.get('category')
                custom_category = form.cleaned_data.get('custom_category')
                
                if 'other' in category:
                    product.category = custom_category
                product.save() 
                return redirect('vendor_dashboard:vendor_dashboard')
            else:
                error_message = f"Error! Please check your inputs."
                return render_error_page(request, error_message, status_code=400)
        # except Exception as e:
        #     error_message = f"An unexpected error occurred: {str(e)}"
        #     return render_error_page(request, error_message, status_code=400)
    
@method_decorator(utils.login_required, name='dispatch')
class VendorSoldProducts(View):
    template = app + "sold_products.html"
    model = common_models.Order

    def get(self,request):
        try:
            user = request.user
            order_obj = self.model.objects.filter(vendor = user)
            order_list = []
            product_list = []
            quantity_list = []
            for order in order_obj:
                order_list.append(order)
                products = []
                quantity = []
                for i,j in order.products.items():
                    products.append(i)
                    quantity.append(j)
                product_list.append(products)
                quantity_list.append(quantity)
            order_product_quantity = zip(order_list,product_list,quantity_list)
            data = {
                'order_product_quantity': order_product_quantity,
                }
            return render(request, self.template, data)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class SellProductsList(View):
    template = app + "sell_product_list.html"
    model = common_models.ProductFromVendor

    def get(self,request):
        try:
            user = request.user
            product_objs = self.model.objects.filter(vendor = user)
            return render(request,self.template,{'products':product_objs})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class SearchSellProduct(View):
    template = app + "sell_product_list.html"
    model = common_models.ProductFromVendor

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")

            user = request.user

            if search_by and query:
                if search_by == "id":
                    product_objs = self.model.objects.filter(id = query,vendor = user)
                elif search_by == "name":
                    product_objs = self.model.objects.filter(name__icontains=query,vendor = user)

            context = {
                "products": product_objs,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class UpdateProduct(View):
    template = app + "update_sell_products.html"
    model = common_models.ProductFromVendor
    form_class = common_forms.ProductFromVendorForm
    def get(self,request, product_id):
        try:
            product = get_object_or_404(common_models.ProductFromVendor, id=product_id, vendor=request.user)
            form = self.form_class(instance=product)
            return render(request, self.template, {'form': form, 'product': product})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    def post(self,request, product_id):
        try:
            product = get_object_or_404(common_models.ProductFromVendor, id=product_id, vendor=request.user)
            form = self.form_class(request.POST, request.FILES, instance=product)
            if form.is_valid():
                product = form.save(commit=False)  # Don't save the form yet
                category = form.cleaned_data.get('category')
                custom_category = form.cleaned_data.get('custom_category')
                
                if 'other' in category:
                    product.category = custom_category
                product.save() 
                return redirect('vendor_dashboard:vendor_sell_product_list')
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
@method_decorator(utils.login_required, name='dispatch')
class DeleteSellProduct(View):
    model = common_models.ProductFromVendor

    def get(self,request,product_id):
        try:
            product = get_object_or_404(common_models.ProductFromVendor, id=product_id)
            product.delete()
            return redirect('vendor_dashboard:vendor_sell_product_list')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class VendorDownloadInvoice(View):
    model = common_models.Order
    template = app + "invoice.html"

    def get(self,request, order_uid):
        try:
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
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
class VendorGardeningProfile(View):
    template = app + "gardening_profile.html"
    model = common_models.GardeningProfile

    def get(self, request):
        try:
            user = request.user
            garden_profile_obj = self.model.objects.filter(user=user).first()
            if garden_profile_obj:
                garden_area = garden_profile_obj.garden_area
                # Assume each tree needs 4 square ft and each pot needs 1 square ft
                trees = garden_area // 4
                pots = garden_area // 1
            return render(request, self.template, locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
class VendorUpdateGardeningProfileView(View):
    template = app + "edit_gardening_profile.html"
    form_class = GardeningForm
    model = common_models.GardeningProfile

    def get(self, request):
        try:
            user = request.user
            garden_profile_obj = self.model.objects.filter(user=user).first()
            form = self.form_class(instance=garden_profile_obj) if garden_profile_obj else self.form_class()
            context = {'form': form}
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            user = request.user

            if form.is_valid():
                garden_area = form.cleaned_data['garden_area']
                number_of_plants = form.cleaned_data['number_of_plants']
                number_of_unique_plants = form.cleaned_data['number_of_unique_plants']
                garden_image = form.cleaned_data['garden_image']

                gardening_obj = self.model.objects.filter(user=user).first()
                changes = []

                if gardening_obj:
                    # Compare fields to see if there are any changes
                    for field_name, value in form.cleaned_data.items():
                        if getattr(gardening_obj, field_name) != value:
                            changes.append(field_name)

                # Handle update request logic
                req_obj = common_models.GardeningProfileUpdateRequest.objects.filter(user=user)
                if req_obj.exists():
                    # If there is already a pending update request, remove it
                    req_obj.delete()

                # Create new update request
                update_request = common_models.GardeningProfileUpdateRequest(
                    user=user,
                    garden_area=garden_area,
                    number_of_plants=number_of_plants,
                    number_of_unique_plants=number_of_unique_plants,
                    garden_image=garden_image,
                    changes=changes
                )
                update_request.save()

                garden_image_url = request.build_absolute_uri(update_request.garden_image.url)

                # Send email notification
                send_template_email(
                    subject='Gardening Profile Update Request Received',
                    template_name='mail_template/gardening_profile_update_request_sent.html',
                    context={
                        'full_name': update_request.user.full_name,
                        'area_for_update': garden_area,
                        'number_of_plants_for_update': number_of_plants,
                        'number_of_unique_plants_for_update': number_of_unique_plants,
                        'garden_image_for_update': garden_image_url,
                        'is_rtg': False
                    },
                    recipient_list=[update_request.user.email]
                )
                return redirect('vendor_dashboard:vendor_gardeningprofile')
            else:
                # If form is invalid, show error message
                return render_error_page(request, 'Invalid form data', status_code=400)

        except ObjectDoesNotExist:
            return render_error_page(request, 'No gardening profile found', status_code=404)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
class AddActivityVendor(View):
    template = app + "add_activity.html"
    form_class = ActivityAddForm
    model = common_models.UserActivity

    def get(self,request):
        try:
            data = {
                'form': self.form_class(),
            }
            return render(request,self.template,data)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    def post(self,request):
        try:
            user = request.user
            form = self.form_class(request.POST,request.FILES)
            if form.is_valid(): 
                activity_title = form.cleaned_data['activity_title']     
                activity_content = form.cleaned_data['activity_content']
                activity_image = form.cleaned_data['activity_image']
                # Save Activity 
                actvtyreqobj=self.model(user = user,activity_title = activity_title,activity_content = activity_content,activity_image = activity_image)
                actvtyreqobj.save()
                activity_image_url = request.build_absolute_uri(actvtyreqobj.activity_image.url)
                send_template_email(
                    subject='Activity Request Recived Successfully.',
                    template_name='mail_template/activity_request_sent.html',
                    context={
                        'full_name':actvtyreqobj.user.full_name,
                        'activity_title':activity_title,
                        'activity_content':activity_content,
                        'activity_image':activity_image_url,
                        },
                    recipient_list=[actvtyreqobj.user.email]
                )
                return redirect('vendor_dashboard:vendor_dashboard')
        except Exception as e:
            error_message = f"Error! Please check your inputs. {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class ActivityList(View):
    template = app + "activity_list.html"
    model = common_models.UserActivity

    def get(self,request):
        try:
            user = request.user
            activities = self.model.objects.filter(user = user,is_accepted = "approved").order_by('-date_time')
            data ={
                    'activities' : activities,
                }
            return render(request,self.template,data)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class AllPosts(View):
    template = app + "posts.html"
    model = common_models.UserActivity
    def get(self,request):
        try:

            # activity = self.model.objects.get(id=7)
            # activity.likes = []
            # activity.save()

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
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@login_required
def plus_like(request):
    try:
        if request.method == 'GET':
            user = request.user
            actvity_id = request.GET['activity_id']
            activity_obj = common_models.UserActivity.objects.get(id = int(actvity_id))
            if user.full_name not in activity_obj.likes:
                activity_obj.likes.append(user.full_name)
            activity_obj.save()
            data={'status':'Product added to wishlist'}
            return JsonResponse(data)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    
@login_required
def minus_like(request):
    try:
        if request.method == 'GET':
            user = request.user
            actvity_id = request.GET['activity_id']
            activity_obj = common_models.UserActivity.objects.get(id = int(actvity_id))
            if user.full_name in activity_obj.likes:
                activity_obj.likes.remove(user.full_name)
            activity_obj.save()
            data={'status':'Product removed from wishlist'}
            return JsonResponse(data)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    
@login_required
def give_comment(request):
    try:
        if request.method == "POST":
            commenter=request.user.full_name
            comment=request.POST["comment"]
            post=request.POST["post"]
            post_obj = common_models.UserActivity.objects.get(id = int(post)) 
        
            comment_data = {
                "id": str(datetime.datetime.now().timestamp()),  # unique ID for the comment
                "commenter": commenter,
                "comment": comment,
                'commenter_id':request.user.id
            }
            post_obj.comments.append(comment_data)
            post_obj.save()
            return redirect('vendor_dashboard:allposts')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    
@login_required
def delete_comment(request, post_id, comment_id):    
    try:
        post_obj = common_models.UserActivity.objects.get(id=post_id)
            
        # Find the comment by its ID
        post_obj.comments = [comment for comment in post_obj.comments if comment["id"] != comment_id]
            
        post_obj.save()
        return redirect('vendor_dashboard:allposts')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@login_required
def get_all_comments(request):
    try:
        post_id = request.GET.get('post_id')
        activity_obj = common_models.UserActivity.objects.filter(id=int(post_id)).first()
        
        comments_data = activity_obj.comments  # Assuming comments_data is a list of dictionaries
        # Prepare the response data
        response_data = {
            'comments': []
        }

        for comment in comments_data:
            # Check if the current user is the commenter
            is_commenter = comment.get('commenter_id') == request.user.id
            # Append the comment along with the is_commenter flag
            response_data['comments'].append({
                **comment,  # Unpack existing comment data
                'is_commenter': is_commenter  # Add the is_commenter flag
            })

        return JsonResponse(response_data, safe=False)
       
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class WalletView(View):
    template = app + "wallet.html"
    model = common_models.ProduceBuy

    def get(self, request):
        user = request.user
        try:
            # Retrieve ProduceBuy transactions
            produce_transactions = self.model.objects.filter(
                (Q(buyer=user) | Q(seller=user)) & 
                Q(buying_status__in=["PaymentDone", "BuyCompleted"])
            ).order_by('-date_time')

            # Retrieve Order transactions
            order_transactions = common_models.Order.objects.filter(
                Q(customer=user) | Q(vendor=user), 
                payment_status="Paid"
            ).order_by('-date')

            # Combine and structure data for rendering
            transactions = []
            for transaction in produce_transactions:
                # Ensure date_time is timezone-aware
                date_time = timezone.make_aware(transaction.date_time) if timezone.is_naive(transaction.date_time) else transaction.date_time
                transactions.append({
                    "type": "ProduceBuy",
                    "object": transaction,
                    "is_purchase": transaction.buyer == user,
                    "date": date_time,
                })

            for transaction in order_transactions:
                # Extract the first product name and quantity from order_meta_data
                first_product = list(transaction.order_meta_data['products'].items())[0]
                product_name = first_product[0]
                quantity = first_product[1].get('quantity', 'N/A')

                # Convert Order date to a timezone-aware datetime object
                transaction_date = datetime.combine(transaction.date, time.min)  # Convert date to datetime
                transaction_date = timezone.make_aware(transaction_date) if timezone.is_naive(transaction_date) else transaction_date

                coin_exchange = transaction.order_meta_data.get('coin_exchange', 'N/A')
                
                if isinstance(coin_exchange, str):
                    try:
                        coin_exchange = int(float(coin_exchange))  # Convert to integer if it's a string float
                    except ValueError:
                        coin_exchange = 0
                
                transactions.append({
                    "type": "Order",
                    "object": transaction,
                    "is_purchase": transaction.customer == user,
                    "product_name": product_name,
                    "quantity": quantity,
                    "amount": coin_exchange,
                    "date": transaction_date,
                })

            # Sort transactions by the normalized date field
            transactions.sort(key=lambda x: x["date"], reverse=True)

            return render(request, self.template, {"transactions": transactions})
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)            
    
@method_decorator(utils.login_required, name='dispatch')
class SellProduceView(View):
    template = app + "sell_produce.html"
    form_class = SellProduceForm
    model = common_models.SellProduce

    def get(self,request):
        try:
            data = {
                'form': self.form_class(),
            }
            return render(request,self.template,data)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    def post(self,request):
        try:
            user = request.user
            form = self.form_class(request.POST,request.FILES)
            if form.is_valid(): 
                produce_category = form.cleaned_data['produce_category']
                product_name = form.cleaned_data['product_name'] 
                product_image = form.cleaned_data['product_image']    
                product_quantity = form.cleaned_data['product_quantity']
                SI_units = form.cleaned_data['SI_units']
                amount_in_green_points = form.cleaned_data['amount_in_green_points']
                validity_duration_days = form.cleaned_data['validity_duration_days']

                # Save SellProduce
                
                sellObj=self.model(user = user,produce_category=produce_category,product_name = product_name,product_image = product_image,product_quantity = product_quantity,SI_units = SI_units,amount_in_green_points = amount_in_green_points,validity_duration_days = validity_duration_days)
                sellObj.save()
                produce_image_url = request.build_absolute_uri(sellObj.product_image.url)

                send_template_email(
                    subject='Sell Produce Request Recived Successfully.',
                    template_name='mail_template/sell_produce_request_sent.html',
                    context={
                        'full_name':sellObj.user.full_name,
                        'product_name':sellObj.product_name,
                        'produce_category':produce_category,
                        'product_quantity':sellObj.product_quantity,
                        'SI_units':sellObj.SI_units,
                        'amount_in_green_points':sellObj.amount_in_green_points,
                        'validity_duration_days':sellObj.validity_duration_days,
                        'product_image':produce_image_url,
                        },
                    recipient_list=[sellObj.user.email]
                )
                return redirect('vendor_dashboard:vendor_dashboard')
        except Exception as e:
            error_message = f"Error! Please check your inputs. {str(e)}"
            return render_error_page(request, error_message, status_code=400)


def delete_expired_sell_produce(request):
    """
    This function is used to delete the expired sell produce from database.
    It will be called in every midnight by a cron job.
    0 0 * * * /path/to/python /path/to/your/manage.py shell -c "from yourapp.utils import delete_expired_sell_produce; delete_expired_sell_produce()"
    """
    current_date = timezone.now()
    common_models.SellProduce.objects.filter(validity__lte=current_date).delete()
   

@method_decorator(utils.login_required, name='dispatch')
class AllSellRequests(View):
    template = app + "sellrequestlist.html"
    model = common_models.SellProduce
    def get(self,request):
        try:
            user = request.user
            sell_objs = self.model.objects.filter(user=user).order_by("-id")
            return render(request,self.template,locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class GreenCommerceProductCommunity(View):
    template = app + "greencommerceproducts.html"
    model = common_models.SellProduce
    form = BuyQuantityForm

    def get(self, request):
        try:
            # Fetch all produce categories
            produces_categories = common_models.CategoryForProduces.objects.all()
            
            # Get selected category and search query from request
            selected_category = request.GET.get('category')
            search_query = request.GET.get('search_query', '')
            selected_category_name = ""
            
            # Determine selected category name if applicable
            if selected_category and selected_category != "all":
                selected_category_name = common_models.CategoryForProduces.objects.get(id=selected_category).category_name
            
            # Update expiration status for all produce items
            sell_produce_obj = self.model.objects.all()
            for produce in sell_produce_obj:
                try:
                    produce.days_left_to_expire()
                except Exception as update_error:
                    print(f"Error updating expiration for produce {produce.id}: {update_error}")

            # Filter produce items that are approved and not posted by the current user
            produce_query = self.model.objects.exclude(user=request.user).filter(is_approved="approved")
            print(produce_query)

            # Apply filters based on category and search query
            if selected_category and selected_category != "all":
                produce_query = produce_query.filter(produce_category=selected_category)
            if search_query:
                produce_query = produce_query.filter(product_name__icontains=search_query)

            # Order by latest date and fetch the list of produce objects
            produce_obj = produce_query.order_by("-date_time")
            # Calculate ratings and check message status for each produce object
            ratings_list = [i.user.calculate_avg_rating() for i in produce_obj]
            message_status = [
                Message.objects.filter(
                    Q(receiver=i.user, sender=request.user) | Q(receiver=request.user, sender=i.user)
                ).exists() for i in produce_obj
            ]

            # Zip the values together for easy iteration in the template
            zipped_value = zip(produce_obj, message_status, ratings_list)

            # Context to be passed to the template
            context = {
                'zipped_value': zipped_value,
                'form': self.form,
                'produces_categories': produces_categories,
                'selected_category_name': selected_category_name,
                "searchquery": search_query
            }
            
            # Render the template with the context
            return render(request, self.template, context)
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class BuyingBegins(View):
    model = common_models.SellProduce
    def post(self, request, prod_id):
        try:
            user = request.user
            buyer = common_models.User.objects.get(id=user.id)
            sell_prod_obj = self.model.objects.get(id=prod_id)
            seller = sell_prod_obj.user
           
            product_quantity = sell_prod_obj.product_quantity
            base_amount_in_green_points = sell_prod_obj.amount_in_green_points
 
            # Validate product_quantity
            if product_quantity is None or product_quantity == 0:
                return render_error_page(request, "Product quantity is not available.", status_code=400)
 
            # Calculate price per unit
            price_per_unit = base_amount_in_green_points / product_quantity
 
            form_data = request.POST
            try:
                quantity = int(form_data['quantity'])
            except (ValueError, KeyError):
                return render_error_page(request, "Invalid quantity input.", status_code=400)
 
            # Check if the requested quantity is available
            if product_quantity >= quantity:
                total_amount = price_per_unit * quantity
 
                buyer_wallet = buyer.wallet or 0.0
 
                # Check if buyer has enough green points
                if buyer_wallet >= total_amount:
                    buying_obj = common_models.ProduceBuy(
                        buyer=buyer,
                        seller=seller,
                        sell_produce=sell_prod_obj,
                        product_name=sell_prod_obj.product_name,
                        SI_units=sell_prod_obj.SI_units,
                        buying_status='BuyInProgress',
                        quantity_buyer_want=quantity,
                        ammount_based_on_quantity_buyer_want=total_amount
                    )
                    buying_obj.save()
 
                    # Send email to the buyer
 
                    send_template_email(
                            subject='Purchase Request Submitted Successfully',
                            template_name='mail_template/purchase_request_buyer.html',
                            context={
                                'full_name': buyer.full_name,
                                'product_name': sell_prod_obj.product_name,
                                'quantity': quantity,
                                # 'SI_units': SI_units,
                            },
                            recipient_list=[buyer.email]
                        )
 
 
                    # Send email to the seller
 
                    send_template_email(
                            subject='New Purchase Request Received',
                            template_name='mail_template/purchase_request_seller.html',
                            context={
                                'full_name': seller.full_name,
                                'product_name': sell_prod_obj.product_name,
                                'buyer_name': buyer.full_name,
                                'quantity': quantity,
                                # 'SI_units': SI_units,
                            },
                            recipient_list=[seller.email]
                        )
 
                    return redirect('vendor_dashboard:vendor_dashboard')
                else:
                    error_message = "You don't have enough green points in your wallet!"
                    return render_error_page(request, error_message, status_code=400)
            else:
                error_message = "The requested amount is not available."
                return render_error_page(request, error_message, status_code=400)
 
        except self.model.DoesNotExist:
            return render_error_page(request, "The product is not available.", status_code=400)
        except common_models.User.DoesNotExist:
            return render_error_page(request, "User does not exist.", status_code=400)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
 
 
@method_decorator(utils.login_required, name='dispatch')
class BuyBeginsSellerView(View):
    template = app + "buyingprogressseller.html"
    model = common_models.ProduceBuy
    form = BuyAmmountForm
    def get(self,request):
        try:
            user = request.user
            bbeigins_obj = self.model.objects.filter(seller=user, buying_status="BuyInProgress")
            form = self.form
            return render(request,self.template,locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
       
@method_decorator(utils.login_required, name='dispatch')
class BuyBeginsBuyerView(View):
    template = app + "buyingprogressbuyer.html"
    model = common_models.ProduceBuy
    def get(self,request):
        try:
            user = request.user
            bbeigins_obj = self.model.objects.filter(buyer=user, buying_status="BuyInProgress")
           
            return render(request,self.template,locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
       
@login_required
def send_payment_link(request, buy_id):
    try:
        if request.method == "POST":
            # Fetch the purchase request
            buy_obj = common_models.ProduceBuy.objects.get(id=buy_id)
 
            # Check if payment link has already been sent
            if buy_obj.payment_link == "Send":
                return render_error_page(request, "Payment link has already been sent for this purchase.", status_code=400)
 
            # Calculate the price per unit and the total amount based on the buyer's quantity
            quantity = buy_obj.quantity_buyer_want
            sell_prod_obj = buy_obj.sell_produce
            total_amount_in_green_points = sell_prod_obj.amount_in_green_points
            total_product_quantity = sell_prod_obj.product_quantity
 
            # Ensure valid quantities
            if total_product_quantity is None or total_product_quantity == 0:
                return render_error_page(request, "Invalid product quantity.", status_code=400)
 
            # Calculate price per unit and total amount
            price_per_unit = total_amount_in_green_points / total_product_quantity
            amount_based_on_buyer_quantity = round(quantity * price_per_unit, 2)
 
            # Use a transaction to ensure atomic update
            with transaction.atomic():
                buy_obj.payment_link = "Send"
                buy_obj.ammount_based_on_quantity_buyer_want = amount_based_on_buyer_quantity
                buy_obj.save()
 
            # Send email notifications to the buyer
            send_template_email(
                subject='New Payment Link Sent',
                template_name='mail_template/payment_link.html',
                context={
                    'full_name': buy_obj.buyer.full_name,
                    'product_name': buy_obj.sell_produce.product_name,
                    'amount': buy_obj.ammount_based_on_quantity_buyer_want,
                },
                recipient_list=[buy_obj.buyer.email]
            )
 
            # Send email notifications to the seller
            send_template_email(
                subject='New Payment Link Sent',
                template_name='mail_template/payment_link_seller.html',
                context={
                    'full_name': buy_obj.seller.full_name,
                    'product_name': buy_obj.sell_produce.product_name,
                    'buyer_name': buy_obj.buyer.full_name,
                    'amount': buy_obj.ammount_based_on_quantity_buyer_want,
                },
                recipient_list=[buy_obj.seller.email]
            )
 
            # Redirect back with a success message
            messages.success(request, "Payment link sent successfully.")
            return redirect('vendor_dashboard:buybeginssellerview')
 
    except common_models.ProduceBuy.DoesNotExist:
        return render_error_page(request, "Purchase request not found.", status_code=404)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@method_decorator(login_required, name='dispatch')
class ProduceBuyView(View):
    model = common_models.ProduceBuy

    def get(self, request, prod_id):
        try:
            user = request.user
            buy_prod_obj = self.model.objects.get(id=prod_id)
            seller = buy_prod_obj.seller
            buyer = buy_prod_obj.buyer
            amount_for_quantity_want = buy_prod_obj.ammount_based_on_quantity_buyer_want
            sell_prod = buy_prod_obj.sell_produce

            # Update buyer's wallet and total investments
            buyer.wallet -= amount_for_quantity_want
            buyer.total_invest += amount_for_quantity_want
            buyer.coins += 50

            # Update seller's wallet and total income
            seller.wallet += amount_for_quantity_want
            seller.total_income += amount_for_quantity_want
            seller.coins += 50

            # Update product quantity and amount in green points
            sell_prod_obj = common_models.SellProduce.objects.get(id=sell_prod.id)
            sell_prod_obj.product_quantity -= buy_prod_obj.quantity_buyer_want
            sell_prod_obj.amount_in_green_points -= amount_for_quantity_want

            # Update the buying status
            buy_prod_obj.buying_status = "BuyCompleted"
            buy_prod_obj.save()
            sell_prod_obj.save()
            buyer.save()
            seller.save()

            # Send email notification for purchase completion using templates
            send_template_email(
                subject='Purchase Completed Successfully',
                template_name='mail_template/purchase_completion_buyer.html',
                context={
                    'full_name': buyer.full_name,
                    'product_name': sell_prod_obj.product_name,
                    'quantity': buy_prod_obj.quantity_buyer_want,
                    'amount': buy_prod_obj.ammount_based_on_quantity_buyer_want,
                    'SI_units': sell_prod_obj.SI_units,
                },
                recipient_list=[buyer.email]
            )

            send_template_email(
                subject='Purchase Completed Successfully',
                template_name='mail_template/purchase_completion_seller.html',
                context={
                    'full_name': seller.full_name,
                    'product_name': sell_prod_obj.product_name,
                    'buyer_name': buyer.full_name,
                    'quantity': buy_prod_obj.quantity_buyer_want,
                    'amount': buy_prod_obj.ammount_based_on_quantity_buyer_want,
                    'SI_units': sell_prod_obj.SI_units,
                },
                recipient_list=[seller.email]
            )

            return redirect('vendor_dashboard:greencommerceproducts')

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@login_required
def reject_buy(request, ord_id):
    try:
        order_obj = common_models.ProduceBuy.objects.get(id=ord_id)
        order_obj.buying_status = "BuyRejected"
        order_obj.save()

        # Send email notification for the rejection using templates
        send_template_email(
            subject='Purchase Request Rejected',
            template_name='mail_template/rejection_notification_buyer.html',
            context={
                'full_name': order_obj.buyer.full_name,
                'product_name': order_obj.sell_produce.product_name,
            },
            recipient_list=[order_obj.buyer.email]
        )

        send_template_email(
            subject='Purchase Request Rejected',
            template_name='mail_template/rejection_notification_seller.html',
            context={
                'full_name': order_obj.seller.full_name,
                'product_name': order_obj.sell_produce.product_name,
                'buyer_name': order_obj.buyer.full_name,
            },
            recipient_list=[order_obj.seller.email]
        )

        return redirect('vendor_dashboard:buybeginssellerview')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    
@method_decorator(utils.login_required, name='dispatch')
class AllOrdersFromCommunity(View):
    template = app + "all_orders_from_community.html"
    model = common_models.ProduceBuy
    
    def get(self, request):
        try:
            orders = self.model.objects.filter(buyer=request.user)
            return render(request , self.template , {'orders' : orders})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class RateOrderFromComunity(View):
    model = common_models.ProduceBuy

    def post(self,request):
        try:
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
            return redirect('vendor_dashboard:allordersfromcommunity')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class AllOrders(View):
    template = app + "order_list.html"
    model = common_models.Order

    def get(self, request):
        try:
            order_list = self.model.objects.filter(vendor=request.user).order_by('-id')
            income =  sum(order.order_value for order in order_list)
            paginated_data = utils.paginate(request, order_list, 50)
            order_status_options = common_models.Order.ORDER_STATUS
            # print(order_list)
            context = {
                "order":order_list,
                "order_list":paginated_data,
                "order_status_options":order_status_options,
                "income":income
            }
            return render(request , self.template , context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class OrderStatusSearch(View):
    model = common_models.Order
    template = app + "order_list.html"

    def get(self,request):
        try:
            filter_by = request.GET.get('filter_by')
            order_list = self.model.objects.filter(vendor = request.user,order_status = filter_by)
            paginated_data = utils.paginate(request, order_list, 50)
            order_status_options = common_models.Order.ORDER_STATUS

            all_order_list = self.model.objects.filter(vendor=request.user).order_by('-id')
            income =  sum(order.order_value for order in all_order_list)
            
            context = {
                "order":order_list,
                "order_list":paginated_data,
                "order_status_options":order_status_options,
                "income":income
            }
            return render(request, self.template,context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class OrderSearch(View):
    model = common_models.Order
    template = app + "order_list.html"

    def get(self,request):
        try:
            query = request.GET.get('query')
            order_list = self.model.objects.filter(uid__icontains = query)
        
            order_status_options = common_models.Order.ORDER_STATUS

            all_order_list = self.model.objects.filter(vendor=request.user).order_by('-id')
            income =  sum(order.order_value for order in all_order_list)
            
            context = {
                "order":order_list,
                "order_list":order_list,
                "order_status_options":order_status_options,
                "income":income
            }
            return render(request, self.template,context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class OrderDetail(View):
    model = common_models.Order
    form_class = OrderUpdateForm
    template= app + "order_detail.html"

    def get(self,request, order_uid):
        try:
            # order_o = common_model.Cart.objects.all().delete()
            order = self.model.objects.get(uid = order_uid)
            
            product_list = []
            product_quantity = []
            total_quantity= 0
            grand_total = 0
            try:
                grand_total = order.order_meta_data['final_cart_value']
            except Exception:
                grand_total = order.order_meta_data['final_value']
            # for product in order.products:
            #     product['product']['quantity'] = product['quantity']
            #     total_quantity += product['quantity']
            #     product_list.append(product['product'])

            for i,j in order.products.items():
                try:
                    p_obj = common_models.ProductFromVendor.objects.filter(name= i).first()
                except Exception:
                    p_obj = ""
                product_list.append(p_obj)
                product_quantity.append(j)
                total_quantity+= int(j)
            zipproduct = zip(product_list, product_quantity)
            context={
                'order':order,
                'grand_total':grand_total,
                'zipproduct':zipproduct,
                'total_quantity':total_quantity,
                'customer_details':order.customer_details,
                'form':OrderUpdateForm(instance = order)
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    def post(self,request, order_uid):
        try:
            order = self.model.objects.get(uid = order_uid)

            form = self.form_class(request.POST, instance = order)

            if form.is_valid():
                obj=form.save()
                # update_order_status.delay(obj.user.email, OrderSerializer(obj).data)
                messages.success(request, 'Order Status is updated....')

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return redirect('vendor_dashboard:order_detail', order_uid = order_uid)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class ServiceProvidersList(View):
    model = common_models.ServiceProviderDetails
    template = app + "service_providers_list.html"

    def get(self,request):
        try:
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
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

# @method_decorator(utils.login_required, name='dispatch')
# class ListOfServicesByServiceProviders(View):
#     template = app + "list_services.html"
#     model = common_models.Service

#     def get(self, request):
#         try:
#             services = self.model.objects.all()
#             return render(request , self.template , {'services' : services})
#         except Exception as e:
#             error_message = f"An unexpected error occurred: {str(e)}"
#             return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class ListOfServicesByServiceProviders(View):
    template = app + "list_services.html"
    service_model = common_models.Service
    category_model = common_models.CategoryForServices

    def get(self, request):
        try:
            category_id = request.GET.get('category_id')  # Get the category from query parameters
            if category_id:
                # If a category is selected, show services within that category
                selected_category = self.category_model.objects.get(id=category_id)
                services = self.service_model.objects.filter(service_type=selected_category)
                return render(request, self.template, {'services': services, 'selected_category': selected_category})
            else:
                # If no category is selected, show the list of categories
                categories = self.category_model.objects.all()
                return render(request, self.template, {'categories': categories})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
class ServiceSearchView(View):
    model = common_models.Service
    template = app + "list_services.html"

    def get(self, request):
        try:
            search_query = request.GET.get('search_query')

            if search_query:
                # Convert the search query to lowercase
                search_query_lower = search_query.lower()

                # Filter services by converting both the name and service_type to lowercase
                services = common_models.Service.objects.annotate(
                    name_lower=Lower('name'),
                    service_type_lower=Lower('service_type')
                ).filter(
                    Q(name_lower__icontains=search_query_lower) | Q(service_type_lower__icontains=search_query_lower)
                )
            else:
                services = common_models.Service.objects.all()

            context = {
                'services': services,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class ServiceDetails(View):
    template = app + "service_details.html"
    model = common_models.Service
    form_class = BookingForm
    def get(self,request, service_id):
        try:
            form = BookingForm()
            service = get_object_or_404(self.model, id=service_id)
            service_booked_obj = common_models.Booking.objects.filter(service = service,gardener = request.user,status = "pending")
            return render(request, self.template, {'service': service,"form":form,"service_booked_obj":service_booked_obj})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    def post(self,request, service_id):
        try:
            form = BookingForm(request.POST)
            service = get_object_or_404(self.model, id=service_id)
            service_booked_obj = common_models.Booking.objects.filter(service = service,gardener = request.user)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.service = service
                booking.gardener = request.user
                booking.save()
                send_template_email(
                    subject="Booking Confirmation",
                    template_name="mail_template/booking_confirmation.html",
                    context = {
                    'gardener_name': request.user.full_name,
                    'service_name': service.service_type,  # Assuming the service has a name attribute
                    },                 
                    recipient_list=[request.user.email]
                )
                return redirect("vendor_dashboard:list_services")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
@method_decorator(utils.login_required, name='dispatch')
class MyBookedServices(View):
    template = app + "my_booked_services.html"
    model = common_models.Booking
    def get(self,request):
        try:
            booked_services = self.model.objects.filter(gardener=request.user).exclude(status="declined")
            # booked_services = self.model.objects.filter(gardener = request.user)
            return render(request, self.template, {'booked_services': booked_services})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@login_required
def vendor_decline_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        if request.user == booking.gardener:
            booking.status = 'declined'
            booking.save()

            send_template_email(
                subject="Booking Declined",
                template_name="mail_template/booking_decline.html",
                context = {
                'gardener_name': request.user.full_name,
                'service_name': booking.service.name,
                },                 
                recipient_list=[request.user.email]
            )
        return redirect('vendor_dashboard:my_booked_services')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
class VendorContactePage(View):
    template = app + "contact.html"
    form = contactForm

    def get(self,request):
        try:
            data = {
                'form': self.form(),
            }
            return render(request,self.template,data)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
    def post(self, request):
        try:
            form = self.form(request.POST)
            if form.is_valid():
                user = request.user

                name = form.cleaned_data['full_name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']

                try:
                    contact_obj = common_models.User_Query(user = user,full_name = name,email = email,subject = subject,message = message)
                    contact_obj.save()
                    send_template_email(
                        subject="Your Query Is Recieved.",
                        template_name="mail_template/query_submit.html",
                        context={
                            'full_name': contact_obj.full_name,
                            "email": contact_obj.email,
                            'message': contact_obj.message
                        },
                        recipient_list=[contact_obj.email]
                    )
                    messages.success(request,'Query send Successfully. We will be in touch soon.')
                    
                except Exception as e:
                    error_message = f"Something went wrong! {str(e)}"
                    return render_error_page(request, error_message, status_code=400)
            
            return redirect('vendor_dashboard:vendor_contact_page')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class QRCodeList(View):
    model = common_models.VendorQRcode
    template = app + "qrcode_list.html"

    def get(self, request):
        try:
            qrcode_list = self.model.objects.all().order_by('-id')

            context = {
                "qrcode_list": qrcode_list,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class QRCodeAdd(View):
    model = common_models.VendorQRcode
    form_class = VendorQRForm
    template = app + "qrcode_add.html"

    def get(self, request):
        try:
            context = {
                "form": self.form_class(),
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                qr_code_instance = form.save(commit=False)  # Don't save to the database yet
                qr_code_instance.vendor = request.user  # Assign the logged-in user as the vendor
                qr_code_instance.save()  # Save to the database
                messages.success(request, "QR code added successfully.")
                return redirect("vendor_dashboard:qrcode_list")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return render(request, self.template, {"form": form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.login_required, name='dispatch')
class QRCodeUpdate(View):
    model = common_models.VendorQRcode
    form_class = VendorQRForm
    template = app + "qrcode_update.html"

    def get(self, request, qrcode_id):
        try:
            qrcode = get_object_or_404(self.model, id=qrcode_id)
            context = {
                "qrcode": qrcode,
                "form": self.form_class(instance=qrcode),
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request, qrcode_id):
        try:
            qrcode = get_object_or_404(self.model, id=qrcode_id)
            form = self.form_class(request.POST, request.FILES, instance=qrcode)

            if form.is_valid():
                form.save()
                messages.success(request, f"QR code ({qrcode_id}) updated successfully.")
                return redirect("vendor_dashboard:qrcode_list")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return render(request, self.template, {"form": form, "qrcode": qrcode})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class QRCodeDelete(View):
    model = common_models.VendorQRcode

    def get(self, request, qrcode_id):
        try:
            qrcode = get_object_or_404(self.model, id=qrcode_id)

            if qrcode.qr_code: 
                image_path = qrcode.qr_code.path
                os.remove(image_path)

            qrcode.delete()
            messages.info(request, 'QR code deleted successfully.')
            return redirect("vendor_dashboard:qrcode_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)