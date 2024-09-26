from django import forms
from django.core.exceptions import ValidationError
from app_common import models

class RtgRegistrationForm(forms.Form):
    # Fields from RegisterForm
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

    # Fields from GardeningForm
    garden_area = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Area In Sqr.ft',
            'required': 'required'
        })
    )

    number_of_plants = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Total No. of Plants',
            'required': 'required'
        })
    )

    number_of_unique_plants = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Unique No. of Plants',
            'required': 'required'
        })
    )

    garden_image = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

    add_green_coins = forms.ChoiceField(
        label='Add Green Coins For User.',
        choices=[
            ('', 'Select Green Coins'),
            (100, '100'),
            (200, '200'),
            (300, '300'),
            (400, '400'),
            (500, '500'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )


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

        # Validation for RegisterForm part
        city = cleaned_data.get("city")
        other_city = cleaned_data.get("other_city")

        if city == "Other" and not other_city:
            self.add_error("other_city", "Please specify your city.")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
    

class VendorRegistrationForm(forms.Form):
    # Fields from RegisterForm
    CITIES = (
        ("Choose City", "Choose City"),
        ("Bhubaneswar", "Bhubaneswar"),
        ("Cuttack", "Cuttack"),
        ("Brahmapur", "Brahmapur"),
        ("Sambalpur", "Sambalpur"),
        ("Jaipur", "Jaipur"),
        ("Other", "Other"),
    )

    BUSINESS_CATEGORIES = (
        ("Choose Business Category", "Choose Business Category"),
        ('plants', 'Plants'),
        ('tools', 'Tools'),
        ('seeds', 'Seeds'),
        ('other', 'Other'),
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

    # Fields from Vendor Details form
    business_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}))
    business_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Address'}))
    business_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Business Description'}))
    business_license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GST Number'}))
    business_category = forms.ChoiceField(choices=BUSINESS_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Business Category'}))
    other_business_category = forms.CharField(
        max_length=100,
        label='Other Bussiness Category',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Your Bussiness Category'
        })
    )
    establishment_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Establishment Year'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website'}))
    established_by = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}))

    add_green_coins = forms.ChoiceField(
        label='Add Green Coins For User.',
        choices=[
            ('', 'Select Green Coins'),
            (100, '100'),
            (200, '200'),
            (300, '300'),
            (400, '400'),
            (500, '500'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )

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

        business_category = cleaned_data.get("business_category")
        other_business_category = cleaned_data.get("other_business_category")

        if city == "Other" and not other_city:
            self.add_error("other_city", "Please specify your city.")

        if business_category == "other" and not other_business_category:
            self.add_error("other_business_category", "Please specify your business category.")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data
    


class ServiceProviderRegistrationForm(forms.Form):
    # Fields from RegisterForm
    CITIES = (
        ("Choose City", "Choose City"),
        ("Bhubaneswar", "Bhubaneswar"),
        ("Cuttack", "Cuttack"),
        ("Brahmapur", "Brahmapur"),
        ("Sambalpur", "Sambalpur"),
        ("Jaipur", "Jaipur"),
        ("Other", "Other"),
    )
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

    # Fields from SP Details form
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

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data