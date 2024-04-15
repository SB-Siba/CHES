from django import forms
from django.contrib.auth.hashers import make_password

from . import models


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["username","password",]
    username = forms.CharField(max_length=255, label='UserName')
    username.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Username',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))




class RegisterForm(forms.ModelForm):
    CITIES = (
        ("Bhubaneswar","Bhubaneswar"),
        ("Cuttack","Cuttack"),
        ("Brahmapur","Brahmapur"),
        ("Puri","Puri"),
        ("Balasore","Balasore"),
    )

    class Meta:
        model = models.User
        fields =["full_name","email","contact","city","password","confirm_password"]

    full_name = forms.CharField(max_length=255, label='Enter Full Name')
    full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Full Name',"required":"required"})

    email = forms.CharField(label='Email')
    email.widget.attrs.update({'class': 'form-control','type':'email', "placeholder":"Enter Email","required":"required"})

    contact = forms.IntegerField(label='Enter Contact Number')
    contact.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Contact Number',"required":"required"})
    
    city = forms.ChoiceField(choices = CITIES)
    city.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Select City',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}))


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password Mismatched")
        
        return cleaned_data
    
class GardeningForm(forms.ModelForm):
    class Meta:
        model = models.GardeningProfile
        fields = ['garden_area','number_of_plants','number_of_unique_plants','garden_image']

    garden_area = forms.IntegerField()
    garden_area.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Area In Sqr.ft',"required":"required"})
    
    number_of_plants = forms.IntegerField()
    number_of_plants.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Total No. of Plants',"required":"required"})

    number_of_unique_plants = forms.IntegerField()
    number_of_unique_plants.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Unique No. of Plants',"required":"required"})

    garden_image = forms.FileField(required= True)
    garden_image.widget.attrs.update({'class': 'form-control','type':'file'})

class GardeningQuizForm(forms.Form):

    q1 = forms.CharField(label='1. What is the process of cutting off dead or overgrown branches called?')
    q1.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Answer here',"required":"required"})

    q2 = forms.CharField(label='2. Which of the following is a perennial flower?')
    q2.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Answer here',"required":"required"})

    q3 = forms.CharField(label='3. What is the best time of day to water plants?')
    q3.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Answer here',"required":"required"})

    q4 = forms.CharField(label='4. Which type of soil holds water the best?')
    q4.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Answer here',"required":"required"})
    
    q5 = forms.CharField(label='5. What is the primary purpose of adding compost to soil?')
    q5.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Answer here',"required":"required"})
    