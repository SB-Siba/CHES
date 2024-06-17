from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib import auth
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.hashers import check_password,make_password

#import requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.http import JsonResponse

from django.views.generic.edit import FormView
from .forms import CustomPasswordResetForm,CustomSetPasswordForm
from django.views.generic.base import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from smtplib import SMTPException
from . import forms
from helpers import utils
from . import models
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

app = "app_common/"


class Register(View):
    model = models.User
    template = app + "authentication/register.html"
    form_class = forms.RegisterForm

    def get(self,request):
        context = {
            'form': self.form_class()
        }

        return render(request, self.template, context)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            contact = form.cleaned_data['contact']
            city = form.cleaned_data['city']

            try:
                user_obj = models.User(full_name = full_name,email = email,contact = contact,city = city)
                if form.cleaned_data['is_rtg']:
                    user_obj.is_rtg = True
                    user_obj.set_password(password)
                    user_obj.save()
                    messages.success(request,"Now Please give your Gardening Details.")
                    return redirect('app_common:gardeningdetails',email)
                elif form.cleaned_data['is_vendor']:
                    user_obj.is_vendor = True
                    user_obj.set_password(password)
                    user_obj.save()
                    messages.success(request,"Now Please give your Vendor Details.")
                    return redirect('app_common:vendordetails',email)
                elif form.cleaned_data['is_serviceprovider']:
                    user_obj.is_serviceprovider = True
                    user_obj.set_password(password)
                    user_obj.save()
                    messages.success(request,"Now Please give your Vendor Details.")
                    return redirect('app_common:serviceproviderdetails',email)
            except:
                messages.error(request,'Failed to register')
                return redirect('app_common:register')
            
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

            return redirect('app_common:register')


class Login(View):
    model=models.User
    template = app + "authentication/login.html"
    form_class = forms.LoginForm

    def get(self,request):
        context = {
            "form": self.form_class
        }
        return render(request, self.template, context)
    
    def post(self,request):
        data=request.POST
        username = data['username']
        password = data['password']

        user=auth.authenticate(email=username, password=password)

        if user is not None:

            if user.is_superuser == True:
                auth.login(request,user) 
                return redirect('admin_dashboard:admin_dashboard')
        
            elif user.is_approved == True and user.is_rtg == True:
                auth.login(request,user)
                return redirect('user_dashboard:user_dashboard')
            
            elif user.is_approved == True and user.is_vendor == True:
                auth.login(request,user)
                return redirect('vendor_dashboard:vendor_dashboard')
            elif user.is_approved == True and user.is_serviceprovider == True:
                auth.login(request,user)
                return redirect('service_provider:service_provider_dash')
            else:
                messages.error(request,"Your account hasn't been approved yet.")
                return redirect('app_common:login')

        else:
            messages.error(request, "Login Failed / You are not approved yet !!!")

        return redirect('app_common:login')

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('app_common:login')
    

class GardeningDetails(View):
    model = models.GardeningProfile
    template = app + "gardening_details.html"
    form_class = forms.GardeningForm

    def get(self,request,u_email):
        print(u_email)
        try:
            user_obj = models.User.objects.get(email = u_email)
            form = self.form_class(instance=user_obj)
            context={'form':form}
        except self.model.DoesNotExist:
            messages.error(request,"No Data Found")
        
        return render(request, self.template, context)     

    def post(self,request,u_email):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user_obj = models.User.objects.get(email = u_email)

            garden_area = form.cleaned_data['garden_area']
            number_of_plants = form.cleaned_data['number_of_plants']
            number_of_unique_plants = form.cleaned_data['number_of_unique_plants']
            garden_image = form.cleaned_data['garden_image']
           

            try:
                gardening_obj = self.model(user = user_obj,garden_area = garden_area,number_of_plants = number_of_plants,number_of_unique_plants = number_of_unique_plants,garden_image = garden_image)
                gardening_obj.save()
                messages.success(request,'Data Added Successfully.Now Please answer these questions.')
                return redirect('app_common:gardeningquiz',u_email)
            except:
                messages.error(request,'Failed to Add data')
                return redirect('app_common:gardeningdetails',u_email)
        else:
            messages.error(request,'Please correct the below errors.')
            return redirect('app_common:gardeningdetails',u_email)


def gardening_quiz_view(request,u_email):
    print(u_email)
    if request.method == 'POST':
        form = forms.GardeningQuizForm(request.POST)
        if form.is_valid():
            user_obj = models.User.objects.get(email = u_email)
            q1 = form.cleaned_data['q1']
            q2 = form.cleaned_data['q2']
            q3 = form.cleaned_data['q3']
            q4 = form.cleaned_data['q4']
            q5 = form.cleaned_data['q5']

            data = {
                'What is the process of cutting off dead or overgrown branches called?':q1,
                'Which of the following is a perennial flower?':q2,
                'What is the best time of day to water plants?':q3,
                'Which type of soil holds water the best?':q4,
                'What is the primary purpose of adding compost to soil?':q5,
            }
            quiz_obj = models.GaredenQuizModel(user = user_obj,questionANDanswer = data)
            
            try:
                user_email = u_email
                subject = "Registration Successfull."
                message = f"""\
                Hii Dear,
                Your account has been created successfully on our site. You can login when admin approve."""
                from_email = "forverify.noreply@gmail.com"
                send_mail(subject, message, from_email,[user_email], fail_silently=False)
                quiz_obj.save()
            except SMTPException as e:
                # Log the error if needed
                print(f"Failed to send email: {e}")
                user_obj.delete()
                return redirect('app_common:register')

            return redirect('app_common:login')
    else:
        form = forms.GardeningQuizForm()
        context={
            "form":form,
            "u_email":u_email
            }
    return render(request, 'app_common/gardening_quiz.html', context)


class VendorDetails(View):
    model = models.VendorDetails
    template = app + "vendor_details.html"
    form_class = forms.VendorDetailsForm

    def get(self,request,u_email):
        print(u_email)
        try:
            user_obj = models.User.objects.get(email = u_email)
            form = self.form_class(instance=user_obj)
            context={'form':form}
        except self.model.DoesNotExist:
            messages.error(request,"No Data Found")
        
        return render(request, self.template, context)     

    def post(self,request,u_email):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_obj = models.User.objects.get(email = u_email)

            business_name = form.cleaned_data['business_name']
            business_address = form.cleaned_data['business_address']
            business_description = form.cleaned_data['business_description']
            business_license_number = form.cleaned_data['business_license_number']
            business_category = form.cleaned_data['business_category']
            establishment_year = form.cleaned_data['establishment_year']
            website = form.cleaned_data['website']
            established_by = form.cleaned_data['established_by']
           

            try:
                vendor_detail_obj = self.model(
                    vendor = user_obj,
                    business_name = business_name,
                    business_address = business_address,
                    business_description = business_description,
                    business_license_number = business_license_number,
                    business_category = business_category,
                    establishment_year = establishment_year,
                    website = website,
                    established_by = established_by
                    )
                
                try:
                    user_email = u_email
                    subject = "Registration Successful."
                    message = (
                        "Hi Dear,\n\n"
                        "Your account has been created successfully on our site. "
                        "You can login when admin approves."
                    )
                    from_email = "forverify.noreply@gmail.com"
                    send_mail(subject, message, from_email, [user_email], fail_silently=False)
                    vendor_detail_obj.save()

                except SMTPException as e:
                    # Log the error if needed
                    print(f"Failed to send email: {e}")
                    user_obj.delete()
                    return redirect('app_common:register')
                return redirect('app_common:login')
            except:
                messages.error(request,'Failed to Add data')
                return redirect('app_common:vendordetails',u_email)
        else:
            messages.error(request,'Please correct the below errors.')
            return redirect('app_common:vendordetails',u_email)
        

class ServiceProviderDetails(View):
    model = models.ServiceProviderDetails
    template = app + "serviceprovider_details.html"
    form_class = forms.ServiceProviderDetailsForm

    def get(self,request,u_email):
        try:
            user_obj = models.User.objects.get(email = u_email)
            form = self.form_class(instance=user_obj)
            context={'form':form}
        except self.model.DoesNotExist:
            messages.error(request,"No Data Found")
        
        return render(request, self.template, context)     

    def post(self,request,u_email):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_obj = models.User.objects.get(email = u_email)

            service_type = form.cleaned_data['service_type']
            service_area = form.cleaned_data['service_area']
            average_cost_per_hour = form.cleaned_data['average_cost_per_hour']
            years_experience = form.cleaned_data['years_experience']
            try:
                service_provider_detail_obj = self.model(
                    provider = user_obj,
                    service_type = service_type,
                    service_area = service_area,
                    average_cost_per_hour = average_cost_per_hour,
                    years_experience = years_experience,
                    )
                try:
                    user_email = u_email
                    subject = "Registration Successfull."
                    message = f"""\
                    Hii Dear,
                    Your account has been created successfully on our site. You can login when admin approve."""
                    from_email = "forverify.noreply@gmail.com"
                    send_mail(subject, message, from_email,[user_email], fail_silently=False)
                    service_provider_detail_obj.save()
                except SMTPException as e:
                    # Log the error if needed
                    print(f"Failed to send email: {e}")
                    user_obj.delete()
                    return redirect('app_common:register')
                
                return redirect('app_common:login')
            except:
                messages.error(request,'Failed to Add data')
                return redirect('app_common:serviceproviderdetails',u_email)
        else:
            messages.error(request,'Please correct the below errors.')
            return redirect('app_common:serviceproviderdetails',u_email)


class Home(View):
    template = app + 'index.html'

    def get(self, request):
        
        return render(
            request,
            self.template
        )
    

class CustomPasswordResetView(FormView):
    template_name = app + "authentication/password_reset.html"
    template_email = app + "authentication/password_reset_email.html"

    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('app_common:password_reset_done')
    token_generator = default_token_generator

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = models.User._default_manager.filter(email=email)
        if users.exists():
            for user in users:
                current_site = get_current_site(self.request)
                mail_subject = 'Password reset link'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = self.token_generator.make_token(user)
                reset_link = reverse_lazy('app_common:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_url = f"{self.request.scheme}://{current_site.domain}{reset_link}"
                message = render_to_string(self.template_email, {
                    'user': user,
                    'reset_url': reset_url,
                })
                text_message = strip_tags(message)
                msg = EmailMultiAlternatives(mail_subject, text_message, 'admin@example.com', [email])
                msg.attach_alternative(message, "text/html")
                msg.send()
        return super().form_valid(form)
    
class CustomPasswordResetDoneView(TemplateView):
    template_name = app + "authentication/password_reset_done.html"

UserModel = get_user_model()

class CustomPasswordResetConfirmView(FormView):
    template_name = app + "authentication/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    token_generator = default_token_generator
    success_url = reverse_lazy('app_common:password_reset_complete')

    def dispatch(self, *args, **kwargs):
        self.user = self.get_user(kwargs['uidb64'])
        if self.user is not None and self.token_generator.check_token(self.user, kwargs['token']):
            return super().dispatch(*args, **kwargs)
        return self.render_to_response(self.get_context_data(validlink=False))

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            return UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            return None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['validlink'] = True if self.user is not None else False
        return context
    
class CustomPasswordResetCompleteView(TemplateView):
    template_name = app + "authentication/password_reset_complete.html"