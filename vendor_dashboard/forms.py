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
    custom_business_category = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify Custom Category'}))


class ProductFromVendorForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'),
        ('plants', 'Plants'),
        ('tools', 'Gardening Tools'),
        ('fertilizers', 'Fertilizers'),
        ('pots_containers', 'Pots & Containers'),
        ('pest_control', 'Pest Control'),
        ('irrigation', 'Irrigation Systems'),
        ('garden_decor', 'Garden Decor'),
        ('other', 'Other'),  # Add 'Other' as an option
    ]
    
    GST_CHOICES = [
        (Decimal('0.00'), '0%'),
        (Decimal('5.00'), '5%'),
        (Decimal('12.00'), '12%'),
        (Decimal('18.00'), '18%'),
        (Decimal('28.00'), '28%'),
    ]

    discount_percentage = forms.DecimalField(
        label='Discount Percentage',
        max_digits=5,
        decimal_places=2,
        initial=Decimal('10.00'),
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gst_rate = forms.ChoiceField(
        label='GST Rate',
        choices=GST_CHOICES,
        initial=Decimal('0.00'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        label='Category',
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'category-select'})
    )
    custom_category = forms.CharField(
        label='Custom Category',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'custom-category-input', 'style': 'display: none;'})
    )

    class Meta:
        model = common_model.ProductFromVendor
        fields = ['name', 'description', 'discount_price', 'max_price', 'image', 'stock', 'category', 'custom_category','discount_percentage', 'gst_rate']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.category not in dict(self.CATEGORY_CHOICES).keys():
                self.fields['category'].initial = 'other'
                self.fields['custom_category'].initial = self.instance.category
            else:
                self.fields['category'].initial = self.instance.category
                self.fields['custom_category'].widget.attrs.update({'style': 'display: none;'})

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom_category = cleaned_data.get('custom_category')

        if category == 'other' and not custom_category:
            self.add_error('custom_category', 'Please provide a custom category.')
        elif category != 'other' and custom_category:
            self.add_error('custom_category', 'Custom category should only be provided if "Other" is selected.')

        return cleaned_data

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get('discount_percentage', Decimal('10.00'))
        if discount_percentage < Decimal('10.00'):
            raise forms.ValidationError("Discount percentage cannot be less than 10.")
        return discount_percentage

    def clean_gst_rate(self):
        gst_rate = Decimal(self.cleaned_data.get('gst_rate', Decimal('0.00')))
        if gst_rate < Decimal('0.00'):
            raise forms.ValidationError("GST rate cannot be negative.")
        return gst_rate