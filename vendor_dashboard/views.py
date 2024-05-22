from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from app_common import models as common_models
from . import forms as common_forms
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from helpers import utils
from chatapp.models import Message

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