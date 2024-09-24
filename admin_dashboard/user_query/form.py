from django import forms
from app_common import models as common_models

class UserQueryReply(forms.ModelForm):
    class Meta:
        model = common_models.User_Query
        fields = ['reply', 'is_solve']

    # Customizing the 'reply' field
    reply = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": "2",
            "placeholder": "Leave a reply here"
        })
    )

    # Customizing the 'is_solve' field (BooleanField)
    is_solved = forms.BooleanField(
        required=False,  # It's optional if you don't want it mandatory
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )