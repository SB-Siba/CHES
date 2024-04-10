from django import forms
from app_common import models as common_models

class UpdateProfileForm(forms.Form):
    full_name = forms.CharField(max_length=255, label='Enter Full Name')
    full_name.widget.attrs.update({'class': 'form-control', 'type': 'text', 'placeholder': 'Full Name', 'required': 'required'})

    email = forms.CharField(label='Email')
    email.widget.attrs.update({'class': 'form-control', 'type': 'email', 'placeholder': 'user@gmail.com', 'required': 'required', 'readonly': 'readonly'})

    contact = forms.IntegerField(label='Enter Contact Number')
    contact.widget.attrs.update({'class': 'form-control', 'type': 'number', 'placeholder': 'Contact Number', 'required': 'required'})

    facebook_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'Facebook Link'}), required=False)
    instagram_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'Instagram Link'}), required=False)
    twitter_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'Twitter Link'}), required=False)
    youtube_link = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control','placeholder': 'Youtube Link'}), required=False)

    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Address here',
    }))

    user_image = forms.FileField(required= False)
    user_image.widget.attrs.update({'class': 'form-control','type':'file'})

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    


class contactForm(forms.Form):
    class Meta:
        model = common_models.User_Query
        fields = ['full_name','email','subject','message']

    full_name = forms.CharField(max_length=255, label='Enter Full Name')
    full_name.widget.attrs.update({'class': 'form-control', 'type': 'text', 'placeholder': 'Full Name', 'required': 'required'})

    email = forms.CharField(label='Email')
    email.widget.attrs.update({'class': 'form-control', 'type': 'email', 'placeholder': 'user@gmail.com', 'required': 'required'})

    subject = forms.CharField(label='Enter Subject')
    subject.widget.attrs.update({'class': 'form-control', 'type': 'text', 'placeholder': 'Subject', 'required': 'required'})

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter message here',
        'required': 'required'
    }))


class ActivityAddForm(forms.Form):
    activity_title = forms.CharField(label="Activity Title",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Activity Title', 'required': 'required'}))
    activity_content = forms.CharField(label="Activity Description",widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter About Activity', 'required': 'required'}))

    activity_image = forms.FileField(required= True)
    activity_image.widget.attrs.update({'class': 'form-control','type':'file'})

class SellProduceForm(forms.ModelForm):
    SI_UNIT_CHOICES = [
        ('Kilogram', 'Kilogram'),
        ('Gram', 'Gram'),
        ('Liter', 'Liter'),
        ('Units', 'Units'),
    ]

    class Meta:
        model = common_models.SellProduce
        fields = ['product_name', 'product_image', 'product_quantity', 'SI_units','ammount_in_green_points','validity_duration_days']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Produce Name'}),
            'product_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Quantity'}),
            'SI_units': forms.Select(attrs={'class': 'form-control'}),
            'ammount_in_green_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'validity_duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    product_image = forms.ImageField(label="Product Image", required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    
