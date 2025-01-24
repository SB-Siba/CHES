from decimal import Decimal
from gettext import translation
from django.http import HttpResponse, JsonResponse
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
from django.utils.decorators import method_decorator
from helpers import utils
from helpers.decorators import login_required
from django.utils.timezone import now
from django.db.models import Sum, F
from datetime import timedelta

app = "service_provider/"



@method_decorator(utils.login_required, name='dispatch')
class ServiceProviderDashboard(View):
    template = app + "home.html"

    def get(self, request):
        try:
            user = request.user
            # Get top 10 service providers
            providers = common_models.User.objects.filter(is_serviceprovider=True)[:10]
            valid_statuses = ["confirmed", "completed"]

            # Calculate earnings for each provider in a given date range
            def calculate_earnings(provider, start_date, end_date):
                bookings = common_models.Booking.objects.filter(
                    service__provider=provider,
                    booking_date__range=(start_date, end_date),
                    status__in=valid_statuses
                ).annotate(earnings=F('service__price_per_hour'))
                return bookings.aggregate(total_earnings=Sum('earnings'))['total_earnings'] or 0

            # Date range for today, this month, and this year
            today = now().date()
            start_of_month = today.replace(day=1)
            start_of_year = today.replace(month=1, day=1)
            start_of_day = now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now().replace(hour=23, minute=59, second=59, microsecond=999999)

            # Get earnings for each provider for today, this month, and this year
            provider_earnings_today = [(provider, calculate_earnings(provider, start_of_day, end_of_day)) for provider in providers]
            provider_earnings_month = [(provider, calculate_earnings(provider, start_of_month, today)) for provider in providers]
            provider_earnings_year = [(provider, calculate_earnings(provider, start_of_year, today)) for provider in providers]

            # Sort providers by earnings
            provider_earnings_today.sort(key=lambda x: x[1], reverse=True)
            provider_earnings_month.sort(key=lambda x: x[1], reverse=True)
            provider_earnings_year.sort(key=lambda x: x[1], reverse=True)

            # Max earnings for percentage calculation
            max_earnings_today = max(provider_earnings_today, key=lambda x: x[1])[1] if provider_earnings_today else 0
            max_earnings_month = max(provider_earnings_month, key=lambda x: x[1])[1] if provider_earnings_month else 0
            max_earnings_year = max(provider_earnings_year, key=lambda x: x[1])[1] if provider_earnings_year else 0

            # Calculate provider percentages for rankings
            provider_percentages_today = [(provider, amount, (amount / max_earnings_today * 100) if max_earnings_today else 0) for provider, amount in provider_earnings_today]
            provider_percentages_month = [(provider, amount, (amount / max_earnings_month * 100) if max_earnings_month else 0) for provider, amount in provider_earnings_month]
            provider_percentages_year = [(provider, amount, (amount / max_earnings_year * 100) if max_earnings_year else 0) for provider, amount in provider_earnings_year]

            # Calculate the logged-in user's earnings for today, this month, and this year
            earnings_today = calculate_earnings(user, start_of_day, end_of_day)
            earnings_month = calculate_earnings(user, start_of_month, today)
            earnings_year = calculate_earnings(user, start_of_year, today)

            # Get the top service providers by coins for leaderboard
            users_orderby_coins = common_models.User.objects.filter(
                Q(is_serviceprovider=True),
                is_approved=True,
                is_superuser=False
            ).order_by('-coins')[:10]
            users_name = [u.full_name for u in users_orderby_coins]
            user_coins = [u.coins for u in users_orderby_coins]

            # Prepare the context
            context = {
                'provider_percentages_today': provider_percentages_today,
                'provider_percentages_month': provider_percentages_month,
                'provider_percentages_year': provider_percentages_year,
                'max_earnings_today': max_earnings_today,
                'max_earnings_month': max_earnings_month,
                'max_earnings_year': max_earnings_year,
                'earnings_today': earnings_today,
                'earnings_month': earnings_month,
                'earnings_year': earnings_year,
                'users_orderby_coins': users_orderby_coins,
                'users_name': users_name,
                'u_coins': user_coins,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.login_required, name='dispatch')
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

@method_decorator(utils.login_required, name='dispatch')
class ServiceProviderUpdateProfileView(View):
    template_name = app + "service_provider_update_profile.html"
    form_class = ServiceProviderUpdateForm
    model = common_models.ServiceProviderDetails

    def get(self, request):
        try:
            service_provider_details = self.model.objects.filter(provider=request.user).first()
            
            if not service_provider_details:
                raise Exception("ServiceProviderDetails object not found for the current user.")
            
            # Handle missing fields with default values
            existing_service_types = service_provider_details.service_type
            existing_service_areas = service_provider_details.service_area
            initial_data = {
                'service_type': existing_service_types,
                'service_area': existing_service_areas,
                'years_experience': getattr(service_provider_details, 'years_experience', 0),  # Default to 0
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

                years_experience = form.cleaned_data['years_experience']
                
                service_provider_details.service_type = service_type
                service_provider_details.service_area = service_area
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

@method_decorator(utils.login_required, name='dispatch')
class ServiceList(View):
    model = common_models.Service
    form_class = ServiceAddForm
    template = app + "service_list.html"

    def get(self, request):
        try:
            search_by = request.GET.get('search_by')
            search_query = request.GET.get('search')

            if search_by and search_query:
                if search_by == "service_type":
                    service_list = self.model.objects.filter(
                        provider=request.user,
                        service_type__icontains=search_query
                    ).order_by('-id')
                elif search_by == "service_type":
                    service_list = self.model.objects.filter(
                        provider=request.user,
                        service_type__icontains=search_query
                    ).order_by('-id')
            else:
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
            form = self.form_class(request.POST, request.FILES)  # Include request.FILES for image fields
            if form.is_valid():
                service = form.save(commit=False)  # Create the instance without saving yet
                service.provider = request.user  # Set the provider

                # Automatically set sp_details based on the provider
                try:
                    service.sp_details = common_models.ServiceProviderDetails.objects.get(provider=request.user)
                except common_models.ServiceProviderDetails.DoesNotExist:
                    service.sp_details = None  # or handle this case as needed

                service.save()  # Save the instance with sp_details
                messages.success(request, f"{service.service_type} is added to the service list.")
                return redirect("service_provider:service_list")
            else:
                # Handle form errors
                return render(request, self.template, {'form': form})
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)



@method_decorator(utils.login_required, name='dispatch')
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
                messages.success(request, f"{request.POST['service_type']} is updated successfully.")
                return redirect("service_provider:service_list")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

        return redirect("service_provider:service_update", service_id=service_id)

@method_decorator(utils.login_required, name='dispatch')
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


@method_decorator(utils.login_required, name='dispatch')
class MyServiceBookings(View):
    model = common_models.Booking
    template = app + "my_service_bookings.html"

    def get(self, request):
        try:
            bookings = self.model.objects.filter(service__provider=request.user)
            
            # Calculate discounted price for each booking if discount applies
            for booking in bookings:
                service = booking.service
                if service.discount_percentage_for_greencoins > 0:
                    # Calculate the discounted price
                    discount_amount = service.price_per_hour * (service.discount_percentage_for_greencoins / Decimal('100.00'))
                    booking.discounted_price = service.price_per_hour - discount_amount
                else:
                    booking.discounted_price = service.price_per_hour  # No discount

            context = {
                "bookings": bookings,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
@login_required
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

@login_required
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

from decimal import Decimal

@login_required
def mark_as_complete_booking(request, booking_id):
    try:
        booking = get_object_or_404(common_models.Booking, id=booking_id)
        
        # Check if the user is the service provider for this booking
        if request.user == booking.service.provider:
            service = booking.service
            discount_amount = float(service.price_per_hour * (Decimal(service.discount_percentage_for_greencoins) / Decimal('100.00')))
            
            # Ensure booking user has enough wallet balance
            booking_user = booking.gardener  # Assuming `gardener` is the user who booked the service
            if booking_user.wallet >= discount_amount:
                # Mark booking as completed
                booking.status = 'completed'
                booking.save()
                
                # Deduct discount from booking user's wallet and update their total investment
                booking_user.wallet -= discount_amount
                booking_user.total_invest += discount_amount
                booking_user.coins += 50  # Assuming 50 coins are rewarded to the booking user
                booking_user.save()
                
                # Add discount amount to provider's wallet and update their total income
                request.user.wallet += discount_amount
                request.user.total_income += discount_amount
                request.user.coins += 50  # Assuming 50 coins are rewarded to the provider
                request.user.save()

                return redirect('service_provider:my_all_bookings')
            else:
                error_message = "Insufficient wallet balance for the booking user to complete the booking."
                return render_error_page(request, error_message, status_code=400)

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        return render_error_page(request, error_message, status_code=400)




@method_decorator(utils.login_required, name='dispatch')
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
        

@method_decorator(utils.login_required, name='dispatch')
class ServiceProviderWalletView(View):
    template = app + "wallet.html"

    def get(self, request):
        user = request.user
        try:
            # Retrieve Booking transactions for the service provider
            booking_transactions = common_models.Booking.objects.filter(
                Q(gardener=user) | Q(service__provider=user), 
                status="completed"
            ).select_related('service').order_by('-booking_date')

            # Structure data for rendering
            transactions = []

            for booking in booking_transactions:
                service = booking.service
                is_consumer = booking.gardener == user
                green_coins = service.green_coins_required if is_consumer else service.green_coins_required

                transactions.append({
                    "type": "Service",
                    "object": booking,
                    "is_purchase": is_consumer,
                    "service_name": service.service_type.service_category,
                    "amount": green_coins,
                    "date": booking.booking_date,
                })

            # Sort transactions by date
            transactions.sort(key=lambda x: x["date"], reverse=True)

            return render(request, self.template, {"transactions": transactions})
        
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
