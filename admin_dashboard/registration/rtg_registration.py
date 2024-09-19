from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views import View

from EmailIntigration.views import send_template_email
from app_common.error import render_error_page
from .forms import RtgRegistrationForm
from app_common.models import User, GardeningProfile, GaredenQuizModel

app = "admin_dashboard/registration/rtg/"

class RtgRegistration(View):
    template_name = app + "rtg_registration.html"

    def get(self, request):
        form = RtgRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RtgRegistrationForm(request.POST, request.FILES)
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
                
                # Add Coins
                add_green_coins = int(form.cleaned_data['add_green_coins'])  # Convert to integer

                # Extracting data for GardeningProfile model
                garden_area = form.cleaned_data['garden_area']
                number_of_plants = form.cleaned_data['number_of_plants']
                number_of_unique_plants = form.cleaned_data['number_of_unique_plants']
                garden_image = form.cleaned_data['garden_image']

                # Save user data
                user = User(
                    full_name=full_name,
                    email=email,
                    contact=contact,
                    city=city,
                    wallet=500 + add_green_coins,  # Now this will work
                    coins=100,
                    is_approved=True,
                    is_rtg=True
                )
                user.set_password(password)
                user.save()

                # Save gardening data
                gardening_data = GardeningProfile.objects.create(
                    user=user,
                    garden_area=garden_area,
                    number_of_plants=number_of_plants,
                    number_of_unique_plants=number_of_unique_plants,
                    garden_image=garden_image,
                )

                # Send registration email
                send_template_email(
                    subject="Registration Successful",
                    template_name="mail_template/registration_mail.html",
                    context={'full_name': full_name, "email": email},
                    recipient_list=[email]
                )

                # Redirect to a success page
                return redirect('admin_dashboard:RTgardeners_list')

            else:
                error_message = f"An unexpected error occurred: {str(form.errors)}"
                return render_error_page(request, error_message, status_code=400)
                
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
