from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as common_models
from . forms import ServiceProviderUpdateForm
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