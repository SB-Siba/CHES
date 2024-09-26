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

app = "service_provider/"

class ServiceProviderDashboard(View):
    template = app + "home.html"

    def get(self, request):
        try:
            user = request.user
            return render(request, self.template)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

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

class ServiceList(View):
    model = common_models.Service
    form_class = ServiceAddForm
    template = app + "service_list.html"

    def get(self, request):
        try:
            # Get the search query from the request
            search_by = request.GET.get('search_by')
            search_query = request.GET.get('search')

            # Filter services based on the search query (by name, description, or service type)
            if search_by and search_query:
                if search_by == "name":
                    service_list = self.model.objects.filter(
                        provider=request.user,
                        name__icontains=search_query
                    ).order_by('-id')
                elif search_by == "service_type":
                    service_list = self.model.objects.filter(
                        provider=request.user,
                        service_type__icontains=search_query
                    ).order_by('-id')
            else:
                # If no search query, return all services
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
            form = self.form_class(request.POST)
            service_type = request.POST.get("service_type")
            name = request.POST.get("name")
            description = request.POST.get("description")
            price_per_hour = request.POST.get("price_per_hour")

            service = self.model(provider=request.user, name=name, description=description, price_per_hour=price_per_hour, service_type=service_type)
            service.save()
            messages.success(request, f"{request.POST['name']} is added to the service list.")
            return redirect("service_provider:service_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

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
                messages.success(request, f"{request.POST['name']} is updated successfully.")
                return redirect("service_provider:service_list")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        return redirect("service_provider:service_update", service_id=service_id)

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

class MyServiceBookings(View):
    model = common_models.Booking
    template = app + "my_service_bookings.html"

    def get(self, request):
        try:
            bookings = self.model.objects.filter(service__provider=request.user)
            context = {
                "bookings": bookings,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

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

def mark_as_complete_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        if request.user == booking.service.provider:
            booking.status = 'completed'
            booking.save()
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)
    return redirect('service_provider:my_all_bookings')


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