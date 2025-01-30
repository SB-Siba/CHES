from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from EmailIntigration.views import send_template_email
from helpers import utils
from app_common import models
from app_common.error import render_error_page
from .import forms
from app_common.forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.db.models import Q
from helpers import utils
from helpers.utils import login_required
app = "admin_dashboard/manage_users/"

@method_decorator(utils.super_admin_only, name='dispatch')
class PendingRtgs(View):
    model = models.User
    template = app + "forapprovertg.html"
    
    def get(self, request):
        try:
            # Get search parameters from the URL
            search_query = request.GET.get('search', '').strip()

            # Check if a search query exists
            if search_query:
                # Filter based on the search query, excluding rejected users
                not_approvedlist = self.model.objects.filter(
                    is_approved=False, 
                    is_rtg=True
                ).exclude(is_rejected=True).filter(
                    Q(full_name__icontains=search_query) | 
                    Q(email__icontains=search_query)
                ).order_by('-id')
            else:
                # If no search query, show all pending RTGs excluding rejected ones
                not_approvedlist = self.model.objects.filter(
                    is_approved=False, 
                    is_rtg=True
                ).exclude(is_rejected=True).order_by('-id')

            # Prepare gardener and garden details
            rtgardener_list = []
            rtgarden_details_list = []
            for i in not_approvedlist:
                rtgardener_list.append(i)
                garden_details = models.GardeningProfile.objects.get(user=i)
                rtgarden_details_list.append(garden_details)

            rtgardener_data = zip(rtgardener_list, rtgarden_details_list)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # Context to pass to the template
        context = {
            'rtgardener_data': rtgardener_data,
            'search_query': search_query  # Retain the search query in the template
        }
        return render(request, self.template, context)



@method_decorator(utils.super_admin_only, name='dispatch')   
class PendingVendors(View):
    model = models.User
    template = app + "forapprovevendor.html"
    
    def get(self, request):
        try:
            # Get search parameters from the URL
            search_query = request.GET.get('search', '').strip()

            # Check if a search query exists
            if search_query:
                # Filter based on search query for email, business name, and business address
                not_approvedlist = self.model.objects.filter(
                    is_approved=False, 
                    is_vendor=True
                ).filter(
                    Q(email__icontains=search_query) | 
                    Q(vendor_details__business_name__icontains=search_query) | 
                    Q(vendor_details__business_address__icontains=search_query)
                ).order_by('-id')
            else:
                # If no search query, show all pending vendors
                not_approvedlist = self.model.objects.filter(
                    is_approved=False, 
                    is_vendor=True
                ).order_by('-id')

            # Prepare vendor and vendor details
            vendor_list = []
            vendor_details_list = []
            for i in not_approvedlist:
                vendor_list.append(i)
                vendor_details = models.VendorDetails.objects.get(vendor=i)
                vendor_details_list.append(vendor_details)

            vendor_data = zip(vendor_list, vendor_details_list)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # Context to pass to the template
        context = {
            'vendor_data': vendor_data,
            'search_query': search_query  # Retain the search query in the template
        }
        return render(request, self.template, context)
    
@method_decorator(utils.super_admin_only, name='dispatch')
class PendingServiceProviders(View):
    model = models.User
    template = app + "forapproveserviceprovider.html"
    
    def get(self, request):
        try:
            # Get search parameters from the URL
            search_query = request.GET.get('search', '').strip()

            # Check if a search query exists
            if search_query:
                # Filter based on the search query for email, service type, service area, and years of experience
                not_approvedlist = self.model.objects.filter(
                    is_approved=False, 
                    is_serviceprovider=True
                ).filter(
                    Q(email__icontains=search_query) | 
                    Q(serviceproviderdetails__service_type__icontains=search_query) |
                    Q(serviceproviderdetails__service_area__icontains=search_query) |
                    Q(serviceproviderdetails__years_experience__icontains=search_query)  # Corrected field name
                ).order_by('-id')
            else:
                # If no search query, show all pending service providers
                not_approvedlist = self.model.objects.filter(
                    is_approved=False, 
                    is_serviceprovider=True
                ).order_by('-id')

            # Prepare service provider and service provider details
            service_provider_list = []
            service_provider_details_list = []
            for i in not_approvedlist:
                service_provider_list.append(i)
                s_provider_details = models.ServiceProviderDetails.objects.filter(provider=i).first()
                service_provider_details_list.append(s_provider_details)

            service_provider_data = zip(service_provider_list, service_provider_details_list)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # Context to pass to the template
        context = {
            'service_provider_data': service_provider_data,
            'search_query': search_query  # Retain the search query in the template
        }
        return render(request, self.template, context)


@method_decorator(utils.super_admin_only, name='dispatch')
class PendingRtgSearch(View):
    template = app + "forapprovertg.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")
            print(search_by,query)
            rtgardener_list = []  
            rtgarden_details_list = []
            if search_by and query:
                if search_by == "email":
                    users = self.model.objects.filter(email__icontains=query,is_rtg = True,is_approved = False)
                    for i in users:
                        rtgardener_list.append(i)
                        garden_details = models.GardeningProfile.objects.get(user=i)
                        rtgarden_details_list.append(garden_details)

                    rtgardener_data = zip(rtgardener_list, rtgarden_details_list)
                elif search_by == "contact":
                    users = self.model.objects.filter(contact__icontains=query,is_rtg = True,is_approved = False)
                    for i in users:
                        rtgardener_list.append(i)
                        garden_details = models.GardeningProfile.objects.get(user=i)
                        rtgarden_details_list.append(garden_details)

                    rtgardener_data = zip(rtgardener_list, rtgarden_details_list)
            

            context = {
                "rtgardener_data": rtgardener_data,
                'form': self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class PendingSpSearch(View):
    template = app + "forapproveserviceprovider.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")
            service_provider_list = []
            service_provider_details_list = []

            if search_by and query:
                if search_by == "email":
                    users = self.model.objects.filter(email__icontains=query,is_approved=False, is_serviceprovider=True)
                    for i in users:
                        service_provider_list.append(i)
                        s_provider_details = models.ServiceProviderDetails.objects.filter(provider=i).first()
                        service_provider_details_list.append(s_provider_details)

                    service_provider_data = zip(service_provider_list, service_provider_details_list)
                elif search_by == "contact":
                    users = self.model.objects.filter(contact__icontains=query,is_serviceprovider = True,is_approved = False)
                    for i in users:
                        service_provider_list.append(i)
                        s_provider_details = models.ServiceProviderDetails.objects.filter(provider=i).first()
                        service_provider_details_list.append(s_provider_details)

                    service_provider_data = zip(service_provider_list, service_provider_details_list)
            context = {
                "service_provider_data": service_provider_data,
                'form': self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    

@method_decorator(utils.super_admin_only, name='dispatch')
class PendingVendorSearch(View):
    template = app + "forapprovevendor.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")

            vendor_list = []
            vendor_details_list = []

            if search_by and query:
                if search_by == "email":
                    users = self.model.objects.filter(email__icontains=query,is_vendor = True,is_approved = False)
                    for i in users:
                        vendor_list.append(i)
                        vendor_details = models.VendorDetails.objects.get(vendor=i)
                        vendor_details_list.append(vendor_details)

                    vendor_data = zip(vendor_list, vendor_details_list)
                elif search_by == "contact":
                    users = self.model.objects.filter(contact__icontains=query,is_vendor = True,is_approved = False)
                    for i in users:
                        vendor_list.append(i)
                        vendor_details = models.VendorDetails.objects.get(vendor=i)
                        vendor_details_list.append(vendor_details)

                    vendor_data = zip(vendor_list, vendor_details_list)

            context = {
                "vendor_data": vendor_data,
                'form': self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)



@login_required       
def ApproveUser(request, pk):
    try:
        user = get_object_or_404(models.User, id=pk)
        coins = request.GET.get('coins', None)
        
        user.is_approved = True
        if coins:
            user.wallet = 500 + int(coins)
        else:
            user.wallet = 500 + user.quiz_score
        user.coins = 100

        # Sending approval email
        send_template_email(
            subject="Successful Approval",
            template_name="mail_template/successfull_approval_mail.html",
            context={'full_name': user.full_name, "email": user.email},
            recipient_list=[user.email]
        )

        # Save the changes to the user
        user.save()

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

    return redirect("admin_dashboard:admin_dashboard")

@login_required
def RejectUser(request, pk):
    user = get_object_or_404(models.User, id=pk)

    if request.method == "POST":
        form = forms.RejectionReasonForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["reason"]

            # Send rejection email
            send_template_email(
                subject="Profile Rejected",
                template_name="mail_template/account_rejected_mail.html",
                context={
                    "full_name": user.full_name,
                    "email": user.email,
                    "reason": reason  # Pass the rejection reason to the email template
                },
                recipient_list=[user.email]
            )

            # Delete the user
            user.is_rejected = True
            user.save()

            return redirect("admin_dashboard:admin_dashboard")
    else:
        form = forms.RejectionReasonForm()

    return render(request, "admin/reject_user.html", {"form": form, "user": user})

class RejectedRtgs(View):
    model = models.User
    template = app + "rejected_rtgs.html"
    
    def get(self, request):
        try:
            # Get all rejected RTGs
            rejected_rtgs = self.model.objects.filter(is_approved=False, is_rtg=True, is_rejected=True).order_by('-id')

            # Prepare gardener and garden details
            rtgardener_list = []
            rtgarden_details_list = []
            for i in rejected_rtgs:
                rtgardener_list.append(i)
                garden_details = models.GardeningProfile.objects.get(user=i)
                rtgarden_details_list.append(garden_details)

            rtgardener_data = zip(rtgardener_list, rtgarden_details_list)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # Context to pass to the template
        context = {
            'rtgardener_data': rtgardener_data,
        }
        return render(request, self.template, context)


class RejectedVendors(View):
    model = models.User
    template = app + "rejected_vendors.html"
    
    def get(self, request):
        try:
            # Get all rejected vendors
            rejected_vendors = self.model.objects.filter(is_approved=False, is_vendor=True, is_rejected=True).order_by('-id')

            # Prepare vendor and vendor details
            vendor_list = []
            vendor_details_list = []
            for i in rejected_vendors:
                vendor_list.append(i)
                vendor_details = models.VendorDetails.objects.get(vendor=i)
                vendor_details_list.append(vendor_details)

            vendor_data = zip(vendor_list, vendor_details_list)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # Context to pass to the template
        context = {
            'vendor_data': vendor_data,
        }
        return render(request, self.template, context)

class RejectedServiceProviders(View):
    model = models.User
    template = app + "rejected_serviceproviders.html"
    
    def get(self, request):
        try:
            # Get all rejected service providers
            rejected_sp = self.model.objects.filter(is_approved=False, is_serviceprovider=True, is_rejected=True).order_by('-id')

            # Prepare service provider and service provider details
            service_provider_list = []
            service_provider_details_list = []
            for i in rejected_sp:
                service_provider_list.append(i)
                s_provider_details = models.ServiceProviderDetails.objects.filter(provider=i).first()
                service_provider_details_list.append(s_provider_details)

            service_provider_data = zip(service_provider_list, service_provider_details_list)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # Context to pass to the template
        context = {
            'service_provider_data': service_provider_data,
        }
        return render(request, self.template, context)


@method_decorator(utils.super_admin_only, name='dispatch')
class ServiceProvidersList(View):
    template = app + "serviceprovider_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            # Get search parameter from the URL
            search_query = request.GET.get('search', '').strip()

            # Check if a search query exists
            if search_query:
                # Filter users based on search query for email, service type, service area, or years of experience
                user_list = self.model.objects.filter(
                    is_approved=True,
                    is_superuser=False,
                    is_serviceprovider=True
                ).filter(
                    Q(email__icontains=search_query) |
                    Q(serviceproviderdetails__service_type__icontains=search_query) |
                    Q(serviceproviderdetails__service_area__icontains=search_query) |
                    Q(serviceproviderdetails__years_experience__icontains=search_query)  # Ensure correct field name
                ).order_by("-id")
            else:
                # If no search query, show all approved service providers
                user_list = self.model.objects.filter(
                    is_approved=True,
                    is_superuser=False,
                    is_serviceprovider=True
                ).order_by("-id")

            # Context to pass to the template
            context = {
                "user_list": user_list,
                "form": self.form_class,
                "search_query": search_query,  # Retain the search query in the template
            }
            return render(request, self.template, context)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
            
                
@method_decorator(utils.super_admin_only, name='dispatch')
class RTGList(View):
    template = app + "rtg_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            # Get the search parameter from the URL
            search_query = request.GET.get('search', '').strip()

            # Check if a search query exists
            if search_query:
                # Filter based on the search query for email, full name, etc.
                user_list = self.model.objects.filter(
                    is_approved=True,
                    is_superuser=False,
                    is_rtg=True
                ).filter(
                    Q(full_name__icontains=search_query) | 
                    Q(email__icontains=search_query)
                ).order_by("-id")
            else:
                # If no search query, show all approved RTGs
                user_list = self.model.objects.filter(
                    is_approved=True,
                    is_superuser=False,
                    is_rtg=True
                ).order_by("-id")

            # Context to pass to the template
            context = {
                "user_list": user_list,
                "form": self.form_class,
                "search_query": search_query,  # Retain the search query in the template
            }
            return render(request, self.template, context)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class VendorList(View):
    template = app + "vendor_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            # Get search parameters from the URL
            search_query = request.GET.get('search', '').strip()

            # Check if a search query exists
            if search_query:
                # Filter based on search query for email, name, or any other vendor-related fields
                user_list = self.model.objects.filter(
                    is_approved=True,
                    is_superuser=False,
                    is_vendor=True
                ).filter(
                    Q(email__icontains=search_query) |
                    Q(full_name__icontains=search_query) |
                    Q(vendor_details__business_name__icontains=search_query)
                ).order_by("-id")
            else:
                # If no search query, show all approved vendors
                user_list = self.model.objects.filter(
                    is_approved=True,
                    is_superuser=False,
                    is_vendor=True
                ).order_by("-id")

            # Prepare context for the template
            context = {
                "user_list": user_list,
                "form": self.form_class,
                "search_query": search_query,  # Retain the search query in the template
            }
            return render(request, self.template, context)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@login_required   
def Delete_Rtg(request, pk):
    user = get_object_or_404(models.User, id=pk)
    try:
        user.delete()
        return redirect("admin_dashboard:RTgardeners_list")
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@login_required
def Delete_Vendor(request, pk):
    user = get_object_or_404(models.User, id=pk)
    try:
        user.delete()
        return redirect("admin_dashboard:vendors_list")
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@login_required
def Delete_Serviceprovider(request, pk):
    user = get_object_or_404(models.User, id=pk)
    try:
        user.delete()
        return redirect("admin_dashboard:serviceproviders_list")
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class UserGardeningDetails(View):
    template = app + "gardening_data.html"

    def get(self, request, pk):
        try:
            user = get_object_or_404(models.User, id=pk)
            gardening_data = get_object_or_404(models.GardeningProfile, user=user)
            return render(request, self.template, locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class VendorDetails(View):
    template = app + "vendor_data.html"

    def get(self, request, pk):
        try:
            user = get_object_or_404(models.User, id=pk)
            vendor_data = get_object_or_404(models.VendorDetails, vendor=user)
            return render(request, self.template, locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    
@method_decorator(utils.super_admin_only, name='dispatch')
class ServiceProviderDetails(View):
    template = app + "service_provider_data.html"

    def get(self, request, pk):
        try:
            user = get_object_or_404(models.User, id=pk)
            serviceprovider_data = get_object_or_404(models.ServiceProviderDetails, provider=user)
            return render(request, self.template, locals())
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')    
class RtgSearchUser(View):
    template = app + "rtg_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")
            print(search_by,query)

            if search_by and query:
                if search_by == "email":
                    users = self.model.objects.filter(email__icontains=query,is_rtg = True,is_approved = True)
                elif search_by == "contact":
                    users = self.model.objects.filter(contact__icontains=query,is_rtg = True,is_approved = True)
            

            context = {
                "user_list": users,
                'form': self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class SpSearchUser(View):
    template = app + "serviceprovider_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")


            if search_by and query:
                if search_by == "email":
                    users = self.model.objects.filter(email__icontains=query,is_serviceprovider = True,is_approved = True)
                elif search_by == "contact":
                    users = self.model.objects.filter(contact__icontains=query,is_serviceprovider = True,is_approved = True)

            context = {
                "user_list": users,
                'form': self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    

@method_decorator(utils.super_admin_only, name='dispatch')
class VendorSearchUser(View):
    template = app + "vendor_list.html"
    model = models.User
    form_class = forms.WalletBalanceAdd

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")


            if search_by and query:
                if search_by == "email":
                    users = self.model.objects.filter(email__icontains=query,is_vendor = True,is_approved = True)
                elif search_by == "contact":
                    users = self.model.objects.filter(contact__icontains=query,is_vendor = True,is_approved = True)

            context = {
                "user_list": users,
                'form': self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
@method_decorator(utils.super_admin_only, name='dispatch')
class RtgWalletBalanceAdd(View):
    model = models.User
    form_class = forms.WalletBalanceAdd

    def post(self, request):
        try:
            user_id = request.POST.get('user_id')
            user_obj = self.model.objects.get(id=user_id)
            user_obj.wallet += float(request.POST.get('wallet'))
            user_obj.save()
            return redirect("admin_dashboard:RTgardeners_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')    
class VendorWalletBalanceAdd(View):
    model = models.User
    form_class = forms.WalletBalanceAdd

    def post(self, request):
        try:
            user_id = request.POST.get('user_id')
            user_obj = self.model.objects.get(id=user_id)
            user_obj.wallet += float(request.POST.get('wallet'))
            user_obj.save()
            return redirect("admin_dashboard:vendors_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')        
class AddUser(View):
    model = models.User
    template = app + "add_user.html"
    form_class = forms.UserAddForm

    def get(self, request):
        context = {
            "form": self.form_class(),
        }
        return render(request, self.template, context)
    
    def post(self, request):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account is created successfully')
                return redirect('admin_dashboard:users_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
                
                context = {
                    "form": self.form_class(data=request.POST),
                }
                return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')        
class QuizAnswers(View):
    model = models.GaredenQuizModel
    template = app + "quiz_view.html"

    def get(self, request, user_id):
        try:
            user_obj = get_object_or_404(models.User, id=user_id)
            quiz = get_object_or_404(self.model, user=user_obj)
            return render(request, self.template, {'user_id': user_id, 'quiz': quiz})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
    def post(self, request, user_id):
        try:
            user_obj = get_object_or_404(models.User, id=user_id)
            quizPoints = request.POST['quizPoints']
            user_obj.quiz_score = int(quizPoints)
            user_obj.save()
            messages.success(request, 'Wallet Balance For Quiz Given Successfully')
            return redirect("admin_dashboard:pending_rtg")
        except Exception as e:
            messages.error(request, 'Error While Giving Wallet Balance For Quiz')
            return redirect("admin_dashboard:quizanswers", user_id=user_id)


@method_decorator(utils.super_admin_only, name='dispatch')
class UserGardeningProfileUpdateRequest(View):
    template = app + "garden_profile_update_request.html"
    model = models.GardeningProfileUpdateRequest

    def get(self, request):
        try:
            profile_update_obj = self.model.objects.all()
            request_prof_objs = []
            original_prof_objs = []
            for i in profile_update_obj:
                request_prof_objs.append(i)
                user = i.user
                # Check if the user has an original gardening profile
                try:
                    original_profile_data = models.GardeningProfile.objects.get(user=user)
                except models.GardeningProfile.DoesNotExist:
                    original_profile_data = None  # Handle case where profile doesn't exist
                original_prof_objs.append(original_profile_data)
            data = zip(request_prof_objs, original_prof_objs)
            return render(request, self.template, {'data': data})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class SearchGardeningProfileUpdateRequest(View):
    template = app + "garden_profile_update_request.html"
    model = models.GardeningProfileUpdateRequest

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")
            data = None

            if search_by and query:
                if search_by == "email":
                    profile_update_obj = self.model.objects.filter(user__email__icontains=query)
                elif search_by == "contact":
                    profile_update_obj = self.model.objects.filter(user__contact__icontains=query)
                else:
                    profile_update_obj = []

                request_prof_objs = []
                original_prof_objs = []

                for i in profile_update_obj:
                    request_prof_objs.append(i)
                    user = i.user
                    # Check if the user has an original gardening profile
                    try:
                        original_profile_data = models.GardeningProfile.objects.get(user=user)
                    except models.GardeningProfile.DoesNotExist:
                        original_profile_data = None  # Handle case where profile doesn't exist
                    original_prof_objs.append(original_profile_data)

                data = zip(request_prof_objs, original_prof_objs)

            context = {
                "data": data,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@login_required    
def ApproveProfile(request, pk):
    try:
        prof_obj = get_object_or_404(models.GardeningProfileUpdateRequest, id=pk)
        user = prof_obj.user

        # Check if the original profile exists, if not, create a new one
        p_obj_for_update, created = models.GardeningProfile.objects.get_or_create(
            user=user,
            defaults={
                'garden_area': prof_obj.garden_area,
                'number_of_plants': prof_obj.number_of_plants,
                'number_of_unique_plants': prof_obj.number_of_unique_plants,
                'garden_image': prof_obj.garden_image
            }
        )

        if not created:  # If the profile already exists, update the fields
            p_obj_for_update.garden_area = prof_obj.garden_area
            p_obj_for_update.number_of_plants = prof_obj.number_of_plants
            p_obj_for_update.number_of_unique_plants = prof_obj.number_of_unique_plants
            p_obj_for_update.garden_image = prof_obj.garden_image

        p_obj_for_update.save()

        # Send approval email
        send_template_email(
            subject="Gardening Profile Updated",
            template_name="mail_template/gardening_profile_approve_mail.html",
            context={'full_name': user.full_name, "email": user.email},
            recipient_list=[user.email]
        )

        # Delete the request after the profile is updated or created
        prof_obj.delete()

        return redirect("admin_dashboard:gardeningprofileupdaterequest")
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)


@login_required
def RejectProfile(request):
    if request.method == "POST":
        try:
            req_id = request.POST['user_id']
            reason = request.POST['reason']
            
            prof_obj = get_object_or_404(models.GardeningProfileUpdateRequest, id=int(req_id))
            user = prof_obj.user

            reject_object = models.GardeningProfileUpdateReject(
                user=user,
                gardening_profile_update_id=prof_obj.id,
                reason=reason
            )

            send_template_email(
                subject="Gardening Profile Rejected",
                template_name="mail_template/gardening_profile_rejected_mail.html",
                context={'full_name': user.full_name, "email": user.email, 'reason': reason},
                recipient_list=[user.email]
            )
            
            reject_object.save()
            prof_obj.delete()
            return redirect("admin_dashboard:gardeningprofileupdaterequest")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class UserActivityRequest(View):
    template = app + "activity_request.html"
    model = models.UserActivity

    def get(self, request):
        try:
            activity_request_obj = self.model.objects.filter(is_accepted='pending').order_by('-date_time')
            return render(request, self.template, {'activity_request_obj': activity_request_obj})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class SearchUsersActivityRequest(View):
    template = app + "activity_request.html"
    model = models.UserActivity

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")


            if search_by and query:
                if search_by == "email":
                    activity_request_obj = self.model.objects.filter(user__email__icontains = query,is_accepted='pending').order_by('-date_time')
                elif search_by == "activity_title":
                    users = self.model.objects.filter(activity_title__icontains=query,is_accepted='pending').order_by('-date_time')

            context = {
                "activity_request_obj": activity_request_obj,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@login_required    
def ApproveActivity(request, pk):
    try:
        req_obj = get_object_or_404(models.UserActivity, id=pk)
        req_obj.is_accepted = "approved"
        user = get_object_or_404(models.User, id=req_obj.user.id)
        user.coins += 100
        send_template_email(
            subject="Activity Approved",
            template_name="mail_template/activity_approval_mail.html",
            context={'full_name': user.full_name, "email": user.email},
            recipient_list=[user.email]
        )
        user.save()
        req_obj.save()
        messages.info(request, "Activity Added successfully.")
        return redirect("admin_dashboard:useractivityrequest")
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)

@login_required
def RejectActivity(request):
    if request.method == "POST":
        try:
            req_id = request.POST['user_id']
            reason = request.POST['reason']
            
            req_obj = get_object_or_404(models.UserActivity, id=int(req_id))
            req_obj.is_accepted = "rejected"
            req_obj.reject_reason = reason
            send_template_email(
                subject="Activity Rejected",
                template_name="mail_template/activity_rejection_mail.html",
                context={'full_name': req_obj.user.full_name, "email": req_obj.user.email, "reason": req_obj.reject_reason},
                recipient_list=[req_obj.user.email]
            )
            req_obj.save()
            return redirect("admin_dashboard:useractivityrequest")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class UserProduceSellRequest(View):
    template = app + "producesellrequest.html"
    model = models.SellProduce

    def get(self, request):
        try:
            produce_sell_request_obj = self.model.objects.filter(is_approved='pending').order_by('-date_time')
            return render(request, self.template, {'produce_sell_request_obj': produce_sell_request_obj})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.super_admin_only, name='dispatch')
class SearchProduceSellRequest(View):
    template = app + "producesellrequest.html"
    model = models.SellProduce

    def get(self, request):
        try:
            search_by = request.GET.get("search_by")
            query = request.GET.get("query")


            if search_by and query:
                if search_by == "email":
                    produce_sell_request_obj = self.model.objects.filter(user__email__icontains = query,is_approved='pending').order_by('-date_time')
                elif search_by == "product_name":
                    produce_sell_request_obj = self.model.objects.filter(product_name__icontains=query,is_approved='pending').order_by('-date_time')

            context = {
                "produce_sell_request_obj": produce_sell_request_obj,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@login_required
def ApproveSellRequest(request):
    if request.method == "POST":
        try:
            sell_id = request.POST.get('sell_id')
            reason = request.POST.get('reason')

            sell_obj = get_object_or_404(models.SellProduce, id=int(sell_id))

            if sell_obj:
                sell_obj.is_approved = "approved"
                sell_obj.reason = reason
                send_template_email(
                    subject="Sell Request Approved",
                    template_name="mail_template/sell_request_approve_mail.html",
                    context={
                        'full_name': sell_obj.user.full_name,
                        'email': sell_obj.user.email,
                        'reason': sell_obj.reason
                    },
                    recipient_list=[sell_obj.user.email]
                )
                sell_obj.save()
            else:
                messages.error(request, 'This account does not exist.')

            return redirect("admin_dashboard:sellrequest")

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@login_required
def RejectSellRequest(request):
    if request.method == "POST":
        try:
            sell_id = request.POST.get('sell_id')
            reason = request.POST.get('reason')

            sell_obj = get_object_or_404(models.SellProduce, id=int(sell_id))

            if sell_obj:
                sell_obj.is_approved = "rejected"
                sell_obj.reason = reason

                send_template_email(
                    subject="Sell Request Rejected",
                    template_name="mail_template/sell_request_reject_mail.html",
                    context={
                        'full_name': sell_obj.user.full_name,
                        'email': sell_obj.user.email,
                        'reason': sell_obj.reason
                    },
                    recipient_list=[sell_obj.user.email]
                )

                sell_obj.save()
            else:
                messages.error(request, 'This account does not exist.')

            return redirect("admin_dashboard:sellrequest")

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

