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


from . import forms
from helpers import utils
from . import models

app = "app_common/"


class Register(View):
    model = models.User
    template = app + "authentication/register.html"
    form_class = forms.RegisterForm

    def get(self,request):
        initial_data = {'invitation_code':request.GET.get('ref_id', None)}
        context = {
            'form': self.form_class(initial= initial_data)
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
                user_obj.set_password(password)
                user_obj.save()
                request.session['full_name'] = full_name
                messages.success(request,"You have registered successfully. Wait for admin's approval.")
                return redirect('app_common:gardeningdetails',email)
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
        
            elif user.is_approved == True:
                auth.login(request,user)
                return redirect('user_dashboard:user_dashboard')
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
                messages.success(request,'Data Added Successfully')
                return redirect('app_common:gardeningquiz',u_email)
            except:
                messages.error(request,'Failed to Add data')
                return redirect('app_common:gardeningdetails')
        else:
            messages.error(request,'Please correct the below errors.')
            return redirect('app_common:gardeningdetails')


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
            quiz_obj.save()

            messages.success(request,f'Wait For Admin Approve Then You Can Login')
            return redirect('app_common:login')
    else:
        form = forms.GardeningQuizForm()
        context={
            "form":form,
            "u_email":u_email
            }
    return render(request, 'app_common/gardening_quiz.html', context)

class Home(View):
    template = app + 'index.html'

    def get(self, request):
        
        return render(
            request,
            self.template
        )