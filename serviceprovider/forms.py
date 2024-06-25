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
    service_type = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = models.Service
        fields = ['name', 'description', 'price_per_hour', 'service_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Text input with form-control class
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Textarea with form-control class
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),  # Number input with form-control class
            'service_type': forms.Select(attrs={'class': 'form-control'}),  # Select dropdown with form-control class
        }
        labels = {
            'service_type': 'Service Type',  # Example label customization
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].widget.attrs['class'] = 'form-control'  # Add form-control class
        provider = self.initial.get('provider') or (self.instance.provider if self.instance.pk else None)
        if provider:
            provider_details = models.ServiceProviderDetails.objects.filter(provider=provider).first()
            if provider_details:
                service_types = [
                    (service_type.strip('[] \'').strip(), service_type.strip('[] \'').strip()) 
                    for service_type in provider_details.service_type.split(',')
                ]
                self.fields['service_type'].choices = service_types
                self.fields['service_type'].initial = self.instance.service_type

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