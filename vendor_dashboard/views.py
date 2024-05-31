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

app = "vendor_dashboard/"

class VendorDashboard(View):
    template = app + "home.html"

    def get(self, request):
        user = request.user 
        return render(request, self.template)

class VendorProfile(View):
    template = app + "vendor_profile.html"

    def get(self, request):
        user = request.user 
        vendor_obj = get_object_or_404(common_models.VendorDetails,vendor = user)
        return render(request, self.template, {'vendor_obj':vendor_obj})
    
class UpdateProfileView(View):
    template_name = app+"vendor_update_profile.html"
    form_class = common_forms.VendorDetailsForm
    model = common_models.VendorDetails
    
    def get(self, request):
        vendor_details = get_object_or_404(self.model, vendor=request.user)
        initial_data = {
        'business_name': vendor_details.business_name,
        'business_address': vendor_details.business_address,
        'business_description': vendor_details.business_description,
        'business_license_number':vendor_details.business_license_number,
        'business_category':vendor_details.business_category,
        'establishment_year':vendor_details.establishment_year,
        'website':vendor_details.website,
        'established_by':vendor_details.established_by,
        }

        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        vendor_details = get_object_or_404(self.model, vendor=request.user)
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            business_name = form.cleaned_data['business_name']
            business_address = form.cleaned_data['business_address']
            business_description = form.cleaned_data['business_description']
            business_license_number = form.cleaned_data['business_license_number']
            business_category = form.cleaned_data['business_category']
            establishment_year = form.cleaned_data['establishment_year']
            website = form.cleaned_data['website']
            established_by = form.cleaned_data['established_by']
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

            messages.success(request, "Your profile has been updated successfully.")
            return redirect('vendor_dashboard:vendor_profile')
        else:
            messages.error(request, "Please correct the errors below.")
            
        return render(request, self.template_name, {'form': form})
        

class VendorSellProduct(View):
    template = app + "vendor_sell_product.html"
    form_class = common_forms.ProductFromVendorForm
    model = common_models.ProductFromVendor

    def get(self,request):
        data = {
            'form': self.form_class(),
        }
        return render(request,self.template,data)
    
    def post(self,request):
        user = request.user
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid(): 
            product = form.save(commit=False)  # Don't save the form yet
            product.vendor = user  # Set the vendor to the current logged-in user
            product.save() 
            messages.success(request,'Request for sell Sent Successfully')
            return redirect('vendor_dashboard:vendor_dashboard')
        else:
            messages.error(request,"Error! Please check your inputs.")
            return redirect('vendor_dashboard:vendor_sell_product')
        
class VendorSellRequests(View):
    template = app + "vendor_sell_requests.html"
    model = common_models.ProductFromVendor

    def get(self,request):
        user = request.user
        req_obj = self.model.objects.filter(Q(vendor = user) | Q(is_approved = "pending"))
        data = {
            'req_obj': req_obj,
            }
        return render(request, self.template, data)
    
class VendorSoldProducts(View):
    template = app + "sold_products.html"
    model = common_models.Order

    def get(self,request):
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
    
class VendorDownloadInvoice(View):
    model = common_models.Order
    template = app + "invoice.html"

    def get(self,request, order_uid):
        order = self.model.objects.get(uid = order_uid)
        data = OrderSerializer(order).data
        products = []
        quantities = []
        price_per_unit = []
        total_prices = []
        for product,p_overview in data['order_meta_data']['products'].items():
            products.append(product)
            quantities.append(p_overview['quantity'])
            price_per_unit.append(p_overview['price_per_unit'])
            total_prices.append(p_overview['total_price'])
            # product['product']['quantity']=product['quantity']
        
        prod_quant = zip(products, quantities,price_per_unit,total_prices)
        try:
            final_total = data['order_meta_data']['final_cart_value']
        except Exception:
            final_total = data['order_meta_data']['final_value']
        
        context ={
            'order':data,
            'details':data['customer_details'],
            'customer':order.customer,
            'vendor':order.vendor,
            'productandquantity':prod_quant,
            'GST':data['order_meta_data']['charges']['GST'],
            'delevery_charge':data['order_meta_data']['charges']['Delivary'],
            'gross_amt':data['order_meta_data']['our_price'],
            'discount':data['order_meta_data']['discount_amount'],
            'final_total':final_total
        }
        return render(request,self.template,context)
    
class AddActivityVendor(View):
    template = app + "add_activity.html"
    form_class = ActivityAddForm
    model = common_models.UserActivity

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
            return redirect('vendor_dashboard:vendor_dashboard')
        else:
            messages.error(request,"Error! Please check your inputs.")
            return redirect('vendor_dashboard:addactivity')


class ActivityList(View):
    template = app + "activity_list.html"
    model = common_models.UserActivity

    def get(self,request):
        user = request.user
        activities = self.model.objects.filter(user = user,is_accepted = "approved").order_by('-date_time')
        data ={
                'activities' : activities,
             }
        return render(request,self.template,data)

class AllPosts(View):
    template = app + "posts.html"
    model = common_models.UserActivity
    def get(self,request):

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
    

def plus_like(request):
    if request.method == 'GET':
        user = request.user
        actvity_id = request.GET['activity_id']
        activity_obj = common_models.UserActivity.objects.get(id = int(actvity_id))
        if user.full_name not in activity_obj.likes:
            activity_obj.likes.append(user.full_name)
        activity_obj.save()
        data={'status':'Product added to wishlist'}
        return JsonResponse(data)
    
def minus_like(request):
    if request.method == 'GET':
        user = request.user
        actvity_id = request.GET['activity_id']
        activity_obj = common_models.UserActivity.objects.get(id = int(actvity_id))
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
        post_obj = common_models.UserActivity.objects.get(id = int(post)) 
    
        comment_data = {
            "commenter": commenter,
            "comment": comment
        }
        post_obj.comments.append(comment_data)
        post_obj.save()
        return redirect('vendor_dashboard:allposts')
    
def get_all_comments(request):
    post_id = request.GET.get('post_id')
    activity_obj = common_models.UserActivity.objects.filter(id=int(post_id)).first()
    if activity_obj:
        comments_data = activity_obj.comments  # Assuming comments_data is a list of dictionaries
        return JsonResponse(comments_data, safe=False)
    else:
        return JsonResponse([], safe=False)


class WalletView(View):
    template = app + "wallet.html"
    model = common_models.ProduceBuy

    def get(self,request):
        user = request.user
        try:
            transactions = self.model.objects.filter((Q(buyer=user) | Q(seller=user)) & Q(buying_status="BuyCompleted")).order_by('-date_time')
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
    form_class = SellProduceForm
    model = common_models.SellProduce

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
            return redirect('vendor_dashboard:vendor_dashboard')
        else:
            messages.error(request,"Error! Please check your inputs.")
            return redirect('vendor_dashboard:sellproduce')


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
        user = request.user
        sell_objs = self.model.objects.filter(user=user).order_by("-id")
        return render(request,self.template,locals())
    
class GreenCommerceProductCommunity(View):
    template = app + "greencommerceproducts.html"
    model = common_models.SellProduce
    form = BuyQuantityForm

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
                    print(e)
                    return redirect('vendor_dashboard:greencommerceproducts')
            else:
                messages.error(request,"The requested amount is not available.")
                return redirect('vendor_dashboard:greencommerceproducts') 
        except self.model.DoesNotExist:
            messages.error(request,"The product is not available.")
            return redirect('vendor_dashboard:greencommerceproducts')



class BuyBeginsSellerView(View):
    template = app + "buyingprogressseller.html"
    model = common_models.ProduceBuy
    form = BuyAmmountForm
    def get(self,request):
        user = request.user
        bbeigins_obj = self.model.objects.filter(seller=user, buying_status="BuyInProgress")
        form = self.form
        return render(request,self.template,locals())
    
class BuyBeginsBuyerView(View):
    template = app + "buyingprogressbuyer.html"
    model = common_models.ProduceBuy
    def get(self,request):
        user = request.user
        bbeigins_obj = self.model.objects.filter(buyer=user, buying_status="BuyInProgress")
        
        return render(request,self.template,locals())
    
def send_payment_link(request,buy_id):
    if request.method == "POST":
        buy_obj = common_models.ProduceBuy.objects.get(id=buy_id)
        form_data = request.POST
        ammount_based_on_buyer_quantity = int(form_data['ammount_based_on_buyer_quantity'])
        buy_obj.payment_link = "Send"
        buy_obj.ammount_based_on_quantity_buyer_want = ammount_based_on_buyer_quantity
        buy_obj.save()

        return redirect('vendor_dashboard:buybeginssellerview')
    


class ProduceBuyView(View):
    model = common_models.ProduceBuy
    def get(self,request,prod_id):
        user = request.user
        buy_prod_obj = self.model.objects.get(id=prod_id)
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
            print(e)
            return redirect('vendor_dashboard:greencommerceproducts')


def reject_buy(request,ord_id):
    order_obj = common_models.ProduceBuy.objects.get(id=ord_id)
    order_obj.buying_status="BuyRejected"
    order_obj.save()
    return redirect('vendor_dashboard:buybeginssellerview')

    

class AllOrders(View):
    template = app + "order_list.html"
    model = common_models.Order

    def get(self, request):
        order_list = self.model.objects.filter(vendor=request.user).order_by('-id')
        paginated_data = utils.paginate(request, order_list, 50)
        order_status_options = common_models.Order.ORDER_STATUS
        print(order_list)
        context = {
            "order":order_list,
            "order_list":paginated_data,
            "order_status_options":order_status_options,
        }
        return render(request , self.template , context)
    

class OrderStatusSearch(View):
    model = common_models.Order
    template = app + "order_list.html"

    def get(self,request):
        filter_by = request.GET.get('filter_by')
        order_list = self.model.objects.filter(vendor = request.user,order_status = filter_by)
        paginated_data = utils.paginate(request, order_list, 50)
        order_status_options = common_models.Order.ORDER_STATUS
        
        context = {
            "order_list":paginated_data,
            "order_status_options":order_status_options,
        }
        return render(request, self.template,context)


class OrderSearch(View):
    model = common_models.Order
    template = app + "order_list.html"

    def get(self,request):
        query = request.GET.get('query')
        order_list = self.model.objects.filter(uid__icontains = query)
        context = {
            "order_list":order_list,
        }
        return render(request, self.template,context)


class OrderDetail(View):
    model = common_models.Order
    form_class = OrderUpdateForm
    template= app + "order_detail.html"

    def get(self,request, order_uid):
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
                p_obj = common_models.ProductFromVendor.objects.get(name= i)
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
    
    def post(self,request, order_uid):
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
