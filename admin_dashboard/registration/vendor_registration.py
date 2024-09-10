from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views import View

from EmailIntigration.views import send_template_email
from app_common.error import render_error_page
from .forms import VendorRegistrationForm
from app_common.models import User, VendorDetails

app = "admin_dashboard/registration/vendor/"

class VendorRegistration(View):
    template_name = app + "vendor_registration.html"

    def get(self, request):
        form = VendorRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = VendorRegistrationForm(request.POST, request.FILES)
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

                # Extracting data for Vendor Details model
                business_name = form.cleaned_data['business_name']
                business_address = form.cleaned_data['business_address']
                business_description = form.cleaned_data['business_description']
                business_license_number = form.cleaned_data['business_license_number']
                business_category = form.cleaned_data['business_category']
                establishment_year = form.cleaned_data['establishment_year']
                website = form.cleaned_data['website']
                established_by = form.cleaned_data['established_by']

                if business_category == "other":
                    business_category = form.cleaned_data['other_business_category']

                # Save user data
                user = User(
                    full_name=full_name,
                    email=email,
                    contact=contact,
                    city=city,
                    wallet=500 + add_green_coins,
                    coins=100,
                    is_approved=True,
                    is_vendor=True
                )
                user.set_password(password)
                user.save()

                # Save vendor data
                vendor_data = VendorDetails.objects.create(
                    vendor=user,
                    business_name=business_name,
                    business_address=business_address,
                    business_description=business_description,
                    business_license_number=business_license_number,
                    business_category=business_category,
                    establishment_year=establishment_year,
                    website=website,
                    established_by=established_by,
                )

                # Send registration email
                send_template_email(
                    subject="Registration Successful",
                    template_name="mail_template/registration_mail.html",
                    context={'full_name': full_name, "email": email},
                    recipient_list=[email]
                )

                # Redirect to a success page
                return redirect('admin_dashboard:vendors_list')

            else:
                # Handle form errors
                print(form.errors)

        except Exception as e:
            # Exception handling with user-friendly error message
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        # If form is not valid, render the template with the form (including errors)
        return render(request, self.template_name, {'form': form})
