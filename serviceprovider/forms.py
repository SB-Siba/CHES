from django import forms
from app_common import models

class ServiceProviderUpdateForm(forms.Form):
    service_type = forms.MultipleChoiceField(
        choices=models.ServiceProviderDetails.SERVICE_TYPES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    service_area = forms.MultipleChoiceField(
        choices=models.ServiceProviderDetails.SERVICE_AREAS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
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
    class Meta:
        model = models.Service
        fields = ['name', 'description', 'price_per_hour']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),
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