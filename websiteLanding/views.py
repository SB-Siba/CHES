from django.shortcuts import redirect, render
from django.views import View
from django.core.mail import send_mail
from app_common.error import render_error_page
from app_common.forms import contactForm
from app_common.models import MediaGallery, User_Query
from django.contrib import messages

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

class GalleryView(View):
    template = app + 'gallery_page.html'  

    def get(self, request):
        try:
            media_items = MediaGallery.objects.all()

            return render(request, self.template, {'media_items': media_items})

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
        
class ContactUsView(View):
    template_name = app + 'contact_us.html'
    form_class = contactForm
    success_url = '/'  # Redirect to homepage or success page after form submission

    def get(self, request, *args, **kwargs):
        # Set initial data based on the user’s authentication status
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.full_name if request.user.full_name else '',
                'email': request.user.email if request.user.email else '',
                'subject': '',
                'message': ''
            }
        else:
            initial_data = {
                'full_name': '',
                'email': '',
                'subject': '',
                'message': ''
            }
        
        # Initialize the form with the initial data
        form = contactForm(initial=initial_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = contactForm(request.POST)

        if form.is_valid():
            # Save the query data
            user_query = User_Query(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )

            # If the user is authenticated, associate the query with the user
            if request.user.is_authenticated:
                user_query.user = request.user
            
            user_query.save()  # Save the query

            # Send a success message and redirect based on authentication status
            if request.user.is_authenticated:
                messages.success(request, 'Your support request has been sent successfully.')
                return redirect('contact_us')  # Or any other appropriate redirect
            else:
                messages.success(request, 'Your message has been sent successfully.')
                return redirect('contact_us')  # Or any other appropriate redirect
        else:
            # If the form is invalid, render the form again with errors
            return render(request, self.template_name, {'form': form})