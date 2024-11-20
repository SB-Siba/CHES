from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from . import models
from .models import NewsActivity, VendorQRcode
from ckeditor.widgets import CKEditorWidget

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["username","password",]
    username = forms.CharField(max_length=255, label='UserName')
    username.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Username',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter Password'}))




class RegisterForm(forms.ModelForm):
    CITIES = (
        ("Choose City", "Choose City"),
        ("Bhubaneswar", "Bhubaneswar"),
        ("Cuttack", "Cuttack"),
        ("Brahmapur", "Brahmapur"),
        ("Sambalpur", "Sambalpur"),
        ("Jaipur", "Jaipur"),
        ("Other", "Other"),
    )

    full_name = forms.CharField(
        max_length=255, 
        label='Enter Full Name', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Full Name', 
            'required': 'required'
        })
    )

    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Email', 
            'required': 'required'
        })
    )

    contact = forms.CharField(
        max_length=10, 
        label='Enter Contact Number', 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contact Number', 
            'required': 'required'
        })
    )

    city = forms.ChoiceField(
        choices=CITIES, 
        label='City', 
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'required': 'required'
        })
    )

    other_city = forms.CharField(
        max_length=100, 
        label='Other City', 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Your City'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Password', 
            'required': 'required'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password', 
            'required': 'required'
        })
    )

    class Meta:
        model = models.User
        fields = ["full_name", "email", "contact", "city", "password", "confirm_password"]

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            email = email.lower()  # Normalize to lowercase

            # Check if email already exists in the database
            if models.User.objects.filter(email=email).exists():
                raise ValidationError("Email is already in use.")

        return email
    
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get("city")
        other_city = cleaned_data.get("other_city")

        if city == "Other" and not other_city:
            self.add_error("other_city", "Please specify your city.")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
    
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs= {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label='Cofirm Password',widget=forms.PasswordInput(attrs= {'autocomplete':'current-password','class':'form-control'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control text-black',
            'placeholder': 'Email Address'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class': 'form-control text-black'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class': 'form-control text-black'}),
        strip=False,
    )

class GardeningForm(forms.ModelForm):
    class Meta:
        model = models.GardeningProfile
        fields = ['gender', 'caste','garden_area','number_of_plants','number_of_unique_plants','garden_image']

    gender = forms.ChoiceField(choices=models.GardeningProfile.GENDER_CHOICES)
    gender.widget.attrs.update({'class': 'form-control','required': 'required'})

    caste = forms.ChoiceField(choices=models.GardeningProfile.CASTE_CHOICES)
    caste.widget.attrs.update({'class': 'form-control','required': 'required'})

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
    BUSINESS_CATEGORIES = (
        ('plants', 'Plants'),
        ('tools', 'Tools'),
        ('seeds', 'Seeds'),
        ('other', 'Other'),
    )
    class Meta:
        model = models.VendorDetails
        fields = ['business_name', 'business_address', 'business_description', 'business_license_number',
                  'business_category', 'establishment_year', 'website', 'established_by']

    business_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}))
    business_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Address'}))
    business_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Business Description'}))
    business_license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number'}))
    business_category = forms.ChoiceField(choices=BUSINESS_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Business Category'}))
    establishment_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Establishment Year'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}))
    established_by = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}))
    custom_business_category = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify Custom Category'}))


class ServiceProviderDetailsForm(forms.ModelForm):
    SERVICE_TYPES = [
        ('Lawn Care', 'Lawn Care'),
        ('Tree Trimming', 'Tree Trimming'),
        ('Garden Design', 'Garden Design'),
        ('Irrigation Systems', 'Irrigation Systems'),
    ]
    SERVICE_AREAS = (
        ("Bhubaneswar", "Bhubaneswar"),
        ("Cuttack", "Cuttack"),
        ("Brahmapur", "Brahmapur"),
        ("Sambalpur", "Sambalpur"),
        ("Jaipur", "Jaipur"),
    )

    class Meta:
        model = models.ServiceProviderDetails
        fields = ['service_type', 'service_area', 'average_cost_per_hour', 'years_experience']

    service_type = forms.MultipleChoiceField(
        choices=SERVICE_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    service_area = forms.MultipleChoiceField(
        choices=SERVICE_AREAS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    add_service_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add More Service Types'})
    )
    add_service_area = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add More Service Areas'})
    )
    average_cost_per_hour = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Average Cost per Hour'})
    )
    years_experience = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'})
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    
 
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)




class contactForm(forms.Form):
    class Meta:
        model = models.User_Query
        fields = ["full_name", "email", "subject", "message"]

    full_name = forms.CharField(max_length=255, label="Enter Full Name")
    full_name.widget.attrs.update(
        {
            "class": "form-control",
            "type": "text",
            "placeholder": "Full Name",
            "required": "required",
        }
    )

    email = forms.CharField(label="Email")
    email.widget.attrs.update(
        {
            "class": "form-control",
            "type": "email",
            "placeholder": "user@gmail.com",
            "required": "required",
        }
    )

    subject = forms.CharField(label="Enter Subject")
    subject.widget.attrs.update(
        {
            "class": "form-control",
            "type": "text",
            "placeholder": "Subject",
            "required": "required",
        }
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter message here",
                "required": "required",
            }
        )
    )

class MediaGalleryForm(forms.ModelForm):
    class Meta:
        model = models.MediaGallery
        fields = ['media_image']  

        widgets = {
            'media_image': forms.FileInput(attrs={'class': 'form-control'}), 

        }



class NewsActivityForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    content = forms.CharField(
        widget=CKEditorWidget(attrs={'class': 'form-control', 'placeholder': 'Enter content'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    type = forms.ChoiceField(
        choices=NewsActivity.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_of_news_or_event = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    class Meta:
        model = NewsActivity
        fields = ['type', 'title', 'date', 'content', 'image', 'date_of_news_or_event']

class VendorQRForm(forms.ModelForm):
    class Meta:
        model = VendorQRcode
        fields = ['qr_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['qr_code'].widget.attrs.update({'class': 'form-control'})