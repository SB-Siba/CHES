from decimal import Decimal
from gettext import translation
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as common_models
from app_common.error import render_error_page
from EmailIntigration.views import send_template_email
from . forms import ServiceProviderUpdateForm,ServiceAddForm
from user_dashboard.serializers import OrderSerializer
from user_dashboard.forms import ActivityAddForm, BuyAmmountForm,SellProduceForm,BuyQuantityForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from helpers import utils
from chatapp.models import Message
from admin_dashboard.orders.forms import OrderUpdateForm
from app_common.forms import contactForm
from django.utils.decorators import method_decorator
from helpers import utils
from helpers.decorators import login_required

app = "service_provider/"

@method_decorator(utils.login_required, name='dispatch')
class ServiceProviderDashboard(View):
    template = app + "home.html"

    def get(self, request):
        try:
            user = request.user
            return render(request, self.template)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class ServiceProviderProfile(View):
    template = app + "service_provider_profile.html"

    def get(self, request):
        try:
            user = request.user
            service_provider_obj = common_models.ServiceProviderDetails.objects.filter(provider=user).first()
            # print(service_provider_obj.service_type,type(service_provider_obj.service_type),service_provider_obj.service_area,type(service_provider_obj.service_area))
            context = {
                "service_provider_obj": service_provider_obj,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class ServiceProviderUpdateProfileView(View):
    template_name = app + "service_provider_update_profile.html"
    form_class = ServiceProviderUpdateForm
    model = common_models.ServiceProviderDetails

    def get(self, request):
        try:
            service_provider_details = self.model.objects.filter(provider=request.user).first()
            # Convert string representation of lists to actual lists
            existing_service_types = service_provider_details.service_type
            existing_service_areas = service_provider_details.service_area
            initial_data = {
                'service_type': existing_service_types,
                'service_area': existing_service_areas,
                'average_cost_per_hour': service_provider_details.average_cost_per_hour,
                'years_experience': service_provider_details.years_experience,
            }
            form = self.form_class(initial=initial_data, 
                                   existing_service_types=existing_service_types, 
                                   existing_service_areas=existing_service_areas)
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request):
        try:
            service_provider_details = get_object_or_404(self.model, provider=request.user)
            form = self.form_class(request.POST, request.FILES,
                                   existing_service_types=service_provider_details.service_type,
                                   existing_service_areas=service_provider_details.service_area)
            if form.is_valid():
                service_type = form.cleaned_data['service_type']
                service_area = form.cleaned_data['service_area']

                # Handle additional service types
                additional_service_type = form.cleaned_data['add_service_type']
                if additional_service_type:
                    additional_service_types = [s.strip() for s in additional_service_type.split(',')]
                    service_type.extend(additional_service_types)

                # Handle additional service areas
                additional_service_area = form.cleaned_data['add_service_area']
                if additional_service_area:
                    additional_service_areas = [a.strip() for a in additional_service_area.split(',')]
                    service_area.extend(additional_service_areas)

                average_cost_per_hour = form.cleaned_data['average_cost_per_hour']
                years_experience = form.cleaned_data['years_experience']
                
                service_provider_details.service_type = service_type
                service_provider_details.service_area = service_area
                service_provider_details.average_cost_per_hour = average_cost_per_hour
                service_provider_details.years_experience = years_experience
                
                # Update user object if needed
                user_obj = get_object_or_404(common_models.User, id=service_provider_details.provider.id)
                if 'image' in request.FILES:
                    user_obj.user_image = request.FILES['image']
                user_obj.save()
                service_provider_details.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('service_provider:service_provider_profile')
            else:
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        return render(request, self.template_name, {'form': form})

@method_decorator(utils.login_required, name='dispatch')
class ServiceList(View):
    model = common_models.Service
    form_class = ServiceAddForm
    template = app + "service_list.html"

    def get(self, request):
        try:
            search_by = request.GET.get('search_by')
            search_query = request.GET.get('search')

            if search_by and search_query:
                if search_by == "service_type":
                    service_list = self.model.objects.filter(
                        provider=request.user,
                        service_type__icontains=search_query
                    ).order_by('-id')
                elif search_by == "service_type":
                    service_list = self.model.objects.filter(
                        provider=request.user,
                        service_type__icontains=search_query
                    ).order_by('-id')
            else:
                service_list = self.model.objects.filter(provider=request.user).order_by('-id')
            
            form = self.form_class(initial={'provider': request.user})
            context = {
                "form": form,
                "service_list": service_list,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)  # Include request.FILES for image fields
            if form.is_valid():
                service = form.save(commit=False)  # Create the instance without saving yet
                service.provider = request.user  # Set the provider

                # Automatically set sp_details based on the provider
                try:
                    service.sp_details = common_models.ServiceProviderDetails.objects.get(provider=request.user)
                except common_models.ServiceProviderDetails.DoesNotExist:
                    service.sp_details = None  # or handle this case as needed

                service.save()  # Save the instance with sp_details
                messages.success(request, f"{service.service_type} is added to the service list.")
                return redirect("service_provider:service_list")
            else:
                # Handle form errors
                return render(request, self.template, {'form': form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)



@method_decorator(utils.login_required, name='dispatch')
class ServiceUpdate(View):
    model = common_models.Service
    form_class = ServiceAddForm
    template = app + "service_update.html"

    def get(self, request, service_id):
        try:
            service = self.model.objects.get(id=service_id)
            context = {
                "form": self.form_class(instance=service),
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request, service_id):
        try:
            service = self.model.objects.get(id=service_id)
            form = self.form_class(request.POST, request.FILES, instance=service)
            if form.is_valid():
                form.save()
                messages.success(request, f"{request.POST['service_type']} is updated successfully.")
                return redirect("service_provider:service_list")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        return redirect("service_provider:service_update", service_id=service_id)

@method_decorator(utils.login_required, name='dispatch')
class ServiceDelete(View):
    model = common_models.Service

    def get(self, request, service_id):
        try:
            service = self.model.objects.get(id=service_id)
            service.delete()
            messages.info(request, "Service is deleted successfully.")
            return redirect("service_provider:service_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
class MyServiceBookings(View):
    model = common_models.Booking
    template = app + "my_service_bookings.html"

    def get(self, request):
        try:
            bookings = self.model.objects.filter(service__provider=request.user)
            
            # Calculate discounted price for each booking if discount applies
            for booking in bookings:
                service = booking.service
                if service.discount_percentage_for_greencoins > 0:
                    # Calculate the discounted price
                    discount_amount = service.price_per_hour * (service.discount_percentage_for_greencoins / Decimal('100.00'))
                    booking.discounted_price = service.price_per_hour - discount_amount
                else:
                    booking.discounted_price = service.price_per_hour  # No discount

            context = {
                "bookings": bookings,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
@login_required
def confirm_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        if request.user == booking.service.provider:
            booking.status = 'confirmed'
            booking.save()
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    return redirect('service_provider:my_all_bookings')

@login_required
def decline_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        if request.user == booking.service.provider:
            booking.status = 'declined'
            booking.save()
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    return redirect('service_provider:my_all_bookings')

from decimal import Decimal

@login_required
def mark_as_complete_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        
        # Check if the user is the service provider for this booking
        if request.user == booking.service.provider:
            # Calculate discount amount and convert to float
            service = booking.service
            discount_amount = float(service.price_per_hour * (Decimal(service.discount_percentage_for_greencoins) / Decimal('100.00')))

            # Ensure provider has enough wallet balance
            if request.user.wallet >= discount_amount:
                # Mark booking as completed
                booking.status = 'completed'
                booking.save()

                # Deduct discount from provider's wallet
                request.user.wallet += discount_amount
                request.user.save()

                return redirect('service_provider:my_all_bookings')
            else:
                # Handle insufficient wallet balance (e.g., display error message)
                error_message = "Insufficient wallet balance to complete the booking."
                return render_error_page(request, error_message, status_code=400)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)




@method_decorator(utils.login_required, name='dispatch')
class SpContactePage(View):
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
                    # Send email notification
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
            
            return redirect('service_provider:sp_contact_page')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        

@method_decorator(utils.login_required, name='dispatch')
class WalletView(View):
    template = app + "wallet.html"
    model = common_models.ProduceBuy

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
            return render(request,self.template,locals())
             
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)