from django.shortcuts import redirect, render
from django.views import View

app = "Landing_Template/"

class WebsiteLanding(View):
    template = app + "website_landing.html"

    def get(self, request):      
        if request.user.is_authenticated:
            if request.user.is_superuser == True:
                return redirect('admin_dashboard:admin_dashboard')
        
            elif request.user.is_approved == True and request.user.is_rtg == True:
                return redirect('user_dashboard:user_dashboard')
            
            elif request.user.is_approved == True and request.user.is_vendor == True:
                return redirect('vendor_dashboard:vendor_dashboard')
            elif request.user.is_approved == True and request.user.is_serviceprovider == True:
                return redirect('service_provider:service_provider_dash')

        # Check if the user has a pending registration step
        if 'registration_step' in request.session and 'registration_email' in request.session:
            step = request.session['registration_step']
            email = request.session['registration_email']

            if step == 'gardeningdetails':
                return redirect('app_common:gardeningdetails', email)
            elif step == 'gardeningquiz':
                return redirect('app_common:gardeningquiz', email)
            elif step == 'vendordetails':
                return redirect('app_common:vendordetails', email)
            elif step == 'serviceproviderdetails':
                return redirect('app_common:serviceproviderdetails', email)
            
        
        return render(request, self.template)

    def post(self, request):
        if 'disclaimer_agreed' in request.POST:
            return redirect('app_common:index')
        
        return render(request, self.template)
