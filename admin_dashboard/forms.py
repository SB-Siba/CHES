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
