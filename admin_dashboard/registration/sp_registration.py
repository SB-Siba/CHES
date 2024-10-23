from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views import View

from EmailIntigration.views import send_template_email
from app_common.error import render_error_page
from .forms import ServiceProviderRegistrationForm
from app_common.models import User, ServiceProviderDetails
from django.utils.decorators import method_decorator
from helpers import utils
app = "admin_dashboard/registration/serviceprovider/"

@method_decorator(utils.super_admin_only, name='dispatch')
class ServiceProviderRegistration(View):
    template_name = app + "sp_registration.html"

    def get(self, request):
        form = ServiceProviderRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ServiceProviderRegistrationForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                # Process the form data
                # Extracting data for User model
                full_name = form.cleaned_data['full_name']
                email = form.cleaned_data['email']
                contact = form.cleaned_data['contact']
                city = form.cleaned_data['city']
                password = form.cleaned_data['password']
                if city == "Other":
                    city = form.cleaned_data['other_city']

                # Extracting data for SP Details model
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

                # Save user data
                user = User(
                    full_name=full_name,
                    email=email,
                    contact=contact,
                    city=city,
                    wallet=500,
                    coins=100,
                    is_approved=True,
                    is_serviceprovider=True
                )
                user.set_password(password)
                user.save()

                # Save service provider details
                service_provider_detail_obj = ServiceProviderDetails.objects.create(
                    provider=user,
                    service_type=service_type,
                    service_area=service_area,
                    average_cost_per_hour=average_cost_per_hour,
                    years_experience=years_experience,
                )

                # Send registration email
                send_template_email(
                    subject="Registration Successful",
                    template_name="mail_template/registration_mail.html",
                    context={'full_name': full_name, "email": email},
                    recipient_list=[email]
                )

                # Redirect to a success page
                return redirect('admin_dashboard:serviceproviders_list')

            else:
                error_message = f"An unexpected error occurred: {str(form.errors)}"
                return render_error_page(request, error_message, status_code=400)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
