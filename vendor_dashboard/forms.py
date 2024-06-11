from django import forms
from app_common import models as common_model
from decimal import Decimal

class VendorDetailsForm(forms.Form):
    BUSINESS_CATEGORIES = (
        ('plants', 'Plants'),
        ('tools', 'Tools'),
        ('seeds', 'Seeds'),
        ('other', 'Other'),
    )
    business_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    business_address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    business_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    business_license_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    business_category = forms.ChoiceField(choices=BUSINESS_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    establishment_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    established_by = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

class ProductFromVendorForm(forms.ModelForm):
    discount_percentage = forms.DecimalField(
        label='Discount Percentage',
        max_digits=5,
        decimal_places=2,
        initial=Decimal('10.00'),  # Set the initial value to 10.00
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = common_model.ProductFromVendor
        fields = ['name', 'description', 'discount_price', 'max_price', 'image', 'stock', 'category', 'discount_percentage']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get('discount_percentage', Decimal('10.00'))
        if discount_percentage < Decimal('10.00'):
            raise forms.ValidationError("Discount percentage cannot be less than 10.")
        return discount_percentage