from django import forms
from app_common import models

class ServiceProviderUpdateForm(forms.Form):
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
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    
class ServiceAddForm(forms.ModelForm):
    service_type = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = models.Service
        fields = ['name', 'description', 'price_per_hour', 'service_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Text input with form-control class
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Textarea with form-control class
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),  # Number input with form-control class
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),  # Select dropdown with form-control class
        }


class BookingForm(forms.ModelForm):
    booking_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )

    class Meta:
        model = models.Booking
        fields = ['booking_date']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }