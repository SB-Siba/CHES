from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as common_models
from . forms import ServiceProviderUpdateForm,ServiceAddForm
from user_dashboard.serializers import OrderSerializer
from user_dashboard.forms import ActivityAddForm, BuyAmmountForm,SellProduceForm,BuyQuantityForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from helpers import utils
from chatapp.models import Message
from admin_dashboard.orders.forms import OrderUpdateForm
import ast
app = "service_provider/"

class ServiceProviderDashboard(View):
    template = app + "home.html"

    def get(self, request):
        user = request.user 
        return render(request, self.template)
    
class ServiceProviderProfile(View):
    template = app + "service_provider_profile.html"

    def get(self, request):
        user = request.user 
        service_provider_obj = get_object_or_404(common_models.ServiceProviderDetails,provider = user)
        context = {
            "service_provider_obj":service_provider_obj,
        }
        return render(request, self.template, context)
    
class ServiceProviderUpdateProfileView(View):
    template_name = app + "service_provider_update_profile.html"
    form_class = ServiceProviderUpdateForm
    model = common_models.ServiceProviderDetails

    def get(self, request):
        service_provider_details = get_object_or_404(self.model, provider=request.user)
        
        # Convert string representation of lists to actual lists
        initial_data = {
            'service_type': ast.literal_eval(service_provider_details.service_type),  # Convert string to list
            'service_area': ast.literal_eval(service_provider_details.service_area),  # Convert string to list
            'average_cost_per_hour': service_provider_details.average_cost_per_hour,
            'years_experience': service_provider_details.years_experience,
        }
        form = self.form_class(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        service_provider_details = get_object_or_404(self.model, provider=request.user)
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Convert form data to string representations of lists
            service_provider_details.service_type = str(form.cleaned_data['service_type'])
            service_provider_details.service_area = str(form.cleaned_data['service_area'])
            service_provider_details.average_cost_per_hour = form.cleaned_data['average_cost_per_hour']
            service_provider_details.years_experience = form.cleaned_data['years_experience']
            
            
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
        
        return render(request, self.template_name, {'form': form})

class ServiceList(View):
    model = common_models.Service
    form_class = ServiceAddForm
    template = app + "service_list.html"

    def get(self,request):
        service_list = self.model.objects.filter(provider = request.user).order_by('-id')
        context = {
            "form": self.form_class,
            "service_list":service_list,
        }
        return render(request, self.template, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_per_hour = form.cleaned_data['price_per_hour']
            service = self.model(provider=request.user, name=name, description=description, price_per_hour=price_per_hour)
            service.save()
            messages.success(request, f"{request.POST['name']} is added to service list.....")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("service_provider:service_list")

class ServiceUpdate(View):
    model = common_models.Service
    form_class = ServiceAddForm
    template = app + "service_update.html"

    def get(self,request, service_id):
        service = self.model.objects.get(id = service_id)
        context = {
            "form": self.form_class(instance=service),
        }
        return render(request, self.template, context)
    
    def post(self, request, service_id):
        service = self.model.objects.get(id= service_id)
        form = self.form_class(request.POST, request.FILES ,instance= service)
        if form.is_valid():
            form.save()
            messages.success(request, f"{request.POST['name']} is updated successfully.....")
            return redirect("service_provider:service_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("service_provider:service_update", service_id = service_id)


class ServiceDelete(View):
    model = common_models.Service

    def get(self,request, service_id):
        service = self.model.objects.get(id= service_id).delete()
        messages.info(request, "Service is deleted successfully....")
        return redirect("service_provider:service_list")
    
class MyServiceBookings(View):
    model = common_models.Booking
    template = app + "my_service_bookings.html"
    def get(self,request):
        bookings = self.model.objects.filter(service__provider=request.user)
        context = {
            "bookings": bookings,
            }
        return render(request, self.template, context)

def confirm_booking(request, booking_id):
    booking = get_object_or_404(common_models.Booking, id=booking_id)
    if request.user == booking.service.provider:
        booking.status = 'confirmed'
        booking.save()
    return redirect('service_provider:my_all_bookings')

def decline_booking(request, booking_id):
    booking = get_object_or_404(common_models.Booking, id=booking_id)
    if request.user == booking.service.provider:
        booking.status = 'declined'
        booking.save()
    return redirect('service_provider:my_all_bookings')