import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as common_models
from user_dashboard.serializers import OrderSerializer
from user_dashboard.forms import ActivityAddForm, BuyAmmountForm,SellProduceForm,BuyQuantityForm
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

app = "vendor_dashboard/"

class VendorDashboard(View):
    template = app + "home.html"

    def get(self, request):
        try:
            user = request.user 
            vendors = common_models.User.objects.filter(is_vendor=True)[:5]
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
                Q(is_rtg=True) | Q(is_vendor=True),
                is_approved=True,
                is_superuser=False
            ).order_by('-coins')[:5]
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
        

class VendorSellProduct(View):
    template = app + "vendor_sell_product.html"
    form_class = common_forms.ProductFromVendorForm
    model = common_models.ProductFromVendor

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
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
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
                messages.success(request,'Request Sent Successfully')
                return redirect('vendor_dashboard:vendor_dashboard')
        except Exception as e:
            error_message = f"Error! Please check your inputs. {str(e)}"
            return render_error_page(request, error_message, status_code=400)


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
                "comment": comment
            }
            post_obj.comments.append(comment_data)
            post_obj.save()
            return redirect('vendor_dashboard:allposts')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    
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

def get_all_comments(request):
    try:
        post_id = request.GET.get('post_id')
        activity_obj = common_models.UserActivity.objects.filter(id=int(post_id)).first()
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
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

class WalletView(View):
    template = app + "wallet.html"
    model = common_models.ProduceBuy

    def get(self,request):
        try:
            user = request.user
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
            return render(request,self.template,locals())
            
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
            
    


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
        
class BuyingBegins(View):
    model = common_models.SellProduce
    
    def post(self,request,prod_id):
        user = request.user
        try:
            buyer = common_models.User.objects.get(id = user.id)
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
                        buying_obj = common_models.ProduceBuy(buyer = buyer,seller = seller,sell_produce = sell_prod_obj,product_name = sell_prod_obj.product_name,SI_units = SI_units,buying_status = 'BuyInProgress',quantity_buyer_want = quantity)
                        buying_obj.save()
                        return redirect('vendor_dashboard:vendor_dashboard')
                    else:
                        messages.error(request,"You don't have enough green points in your wallet!")
                        return redirect('vendor_dashboard:greencommerceproducts')
                except Exception as e:
                    error_message = f"An unexpected error occurred: {str(e)}"
                    return render_error_page(request, error_message, status_code=400)
            else:
                error_message = f"The requested amount is not available."
                return render_error_page(request, error_message, status_code=400)
        except self.model.DoesNotExist:
            error_message = f"The product is not available."
            return render_error_page(request, error_message, status_code=400)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)



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
        
def send_payment_link(request,buy_id):
    try:
        if request.method == "POST":
            buy_obj = common_models.ProduceBuy.objects.get(id=buy_id)
            form_data = request.POST
            ammount_based_on_buyer_quantity = int(form_data['ammount_based_on_buyer_quantity'])
            buy_obj.payment_link = "Send"
            buy_obj.ammount_based_on_quantity_buyer_want = ammount_based_on_buyer_quantity
            buy_obj.save()

            return redirect('vendor_dashboard:buybeginssellerview')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)


class ProduceBuyView(View):
    model = common_models.ProduceBuy
    def get(self,request,prod_id):
        try:
            user = request.user
            buy_prod_obj = self.model.objects.get(id=prod_id)
            seller = buy_prod_obj.seller
            buyer = buy_prod_obj.buyer
            ammount_for_quantity_want = buy_prod_obj.ammount_based_on_quantity_buyer_want
            sell_prod = buy_prod_obj.sell_produce

            buyer.wallet -= ammount_for_quantity_want
            buyer.total_invest += ammount_for_quantity_want
            buyer.coins += 50
                
            seller.wallet += ammount_for_quantity_want
            seller.total_income += ammount_for_quantity_want
            seller.coins += 50

            sell_prod_obj = common_models.SellProduce.objects.get(id = sell_prod.id)
            sell_prod_obj.product_quantity = sell_prod_obj.product_quantity-buy_prod_obj.quantity_buyer_want
            sell_prod_obj.ammount_in_green_points = sell_prod_obj.ammount_in_green_points - ammount_for_quantity_want
            buy_prod_obj.buying_status = "BuyCompleted"
            buy_prod_obj.save()
            sell_prod_obj.save()
            buyer.save()
            seller.save()
            return redirect('vendor_dashboard:greencommerceproducts')  

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


def reject_buy(request,ord_id):
    try:
        order_obj = common_models.ProduceBuy.objects.get(id=ord_id)
        order_obj.buying_status="BuyRejected"
        order_obj.save()
        return redirect('vendor_dashboard:buybeginssellerview')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    
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

class ListOfServicesByServiceProviders(View):
    template = app + "list_services.html"
    model = common_models.Service

    def get(self, request):
        try:
            services = self.model.objects.all()
            return render(request , self.template , {'services' : services})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
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
                return redirect("vendor_dashboard:list_services")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
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
        
def vendor_decline_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        if request.user == booking.gardener:
            booking.status = 'declined'
            booking.save()
        return redirect('vendor_dashboard:my_booked_services')
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)