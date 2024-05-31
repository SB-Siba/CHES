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
        fields = ["full_name", "email", "contact", "city", "password", "confirm_password", "is_gardener", "is_vendor"]

    full_name = forms.CharField(max_length=255, label='Enter Full Name')
    full_name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Full Name',"required":"required"})

    email = forms.EmailField(label='Email')
    email.widget.attrs.update({'class': 'form-control','type':'email', "placeholder":"Enter Email","required":"required"})

    contact = forms.CharField(max_length=10, label='Enter Contact Number')
    contact.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Contact Number',"required":"required"})
    
    city = forms.ChoiceField(choices=CITIES)
    city.widget.attrs.update({'class': 'form-control','placeholder':'Select City',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}))

    is_gardener = forms.BooleanField(required=False, label='Are you a Gardener?')
    is_gardener.widget.attrs.update({'class': 'form-check-input'})

    is_vendor = forms.BooleanField(required=False, label='Are you a Vendor?')
    is_vendor.widget.attrs.update({'class': 'form-check-input'})

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password Mismatched")

        if not cleaned_data.get("is_gardener") and not cleaned_data.get("is_vendor"):
            raise forms.ValidationError("Please select at least one: Gardener or Vendor.")

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
    

class VendorDetailsForm(forms.ModelForm):
    class Meta:
        model = models.VendorDetails
        fields = ['business_name', 'business_address', 'business_description', 'business_license_number',
                  'business_category', 'establishment_year', 'website', 'established_by']

    business_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}))
    business_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Address'}))
    business_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Business Description'}))
    business_license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business License Number'}))
    business_category = forms.ChoiceField(choices=models.VendorDetails.BUSINESS_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Business Category'}))
    establishment_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Establishment Year'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}))
    established_by = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Established By'}))