from django import forms
from app_common import models

class AddCategoryForProduces(forms.ModelForm):
    class Meta:
        model = models.CategoryForProduces
        fields = ["category_name"]

    category_name = forms.CharField(
        required=True,  # Makes the field mandatory
        label="Enter Category Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Category Name',  # Updated placeholder to be more accurate
        })
    )

class AddCategoryForServices(forms.ModelForm):
    class Meta:
        model = models.CategoryForServices
        fields = ["service_category", "image"]  

    service_category = forms.CharField(
        required=True,
        label="Enter Service Category Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter ServiceCategory Name',
        })
    )
    image = forms.ImageField(
        required=False,  # Optional field
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
        }),
        label="Upload Category Image"
    )
