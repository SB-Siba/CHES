from django import forms
from app_common import models

class ServiceProviderUpdateForm(forms.Form):
    DEFAULT_SERVICE_TYPES = [
        ('Lawn Care', 'Lawn Care'),
        ('Tree Trimming', 'Tree Trimming'),
        ('Garden Design', 'Garden Design'),
        ('Irrigation Systems', 'Irrigation Systems'),
    ]
    DEFAULT_SERVICE_AREAS = [
        ("Bhubaneswar", "Bhubaneswar"),
        ("Cuttack", "Cuttack"),
        ("Brahmapur", "Brahmapur"),
        ("Sambalpur", "Sambalpur"),
        ("Jaipur", "Jaipur"),
    ]

    service_type = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    service_area = forms.MultipleChoiceField(
        choices=[],
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

    def __init__(self, *args, **kwargs):
        self.existing_service_types = kwargs.pop('existing_service_types', [])
        self.existing_service_areas = kwargs.pop('existing_service_areas', [])
        super().__init__(*args, **kwargs)

        # Combine existing service types/areas with default ones
        service_types = list(set(self.DEFAULT_SERVICE_TYPES + [(item, item) for item in self.existing_service_types]))
        service_areas = list(set(self.DEFAULT_SERVICE_AREAS + [(item, item) for item in self.existing_service_areas]))

        # Sort choices alphabetically for consistency
        service_types.sort(key=lambda x: x[1])
        service_areas.sort(key=lambda x: x[1])

        # Set the choices dynamically
        self.fields['service_type'].choices = service_types
        self.fields['service_area'].choices = service_areas


    
class ServiceAddForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = ['name', 'description', 'service_image', 'price_per_hour', 'service_type']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Text input with form-control class
            'description': forms.Textarea(attrs={'class': 'form-control'}),  # Textarea with form-control class
            'service_image': forms.FileInput(attrs={'class': 'form-control'}),  # File input for service image
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),  # Number input with form-control class
            'service_type': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for service type with form-control class
        }

    def __init__(self, *args, **kwargs):
        super(ServiceAddForm, self).__init__(*args, **kwargs)
        self.fields['service_type'].queryset = models.CategoryForServices.objects.all()


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