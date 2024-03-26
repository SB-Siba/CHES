from django import forms
from app_common import models
from django.contrib.auth.hashers import make_password


class WalletBalanceAdd(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["wallet"]

    wallet = forms.FloatField(initial=0.0, required= True, label="Enter Amount" )
    wallet.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Enter Amount'})





class UserEdit(forms.ModelForm):

    TRUE_FALSE = (
        (True, 'Yes'),
        (False, 'No')
    )

    class Meta:
        model = models.User
        fields =["username","contact","wallet","is_game_organizer","is_active"]


    username = forms.CharField(max_length=255, label='Enter UserName')
    username.widget.attrs.update({'class': 'form-control','type':'username',"required":"required"})

    contact = forms.CharField(max_length=255, label='Contact Number')
    contact.widget.attrs.update({'class': 'form-control','type':'number',"required":"required"})

    wallet = forms.FloatField(initial= 0.0)
    wallet.widget.attrs.update({'class': 'form-control','type':'number',"required":"required"})

    is_game_organizer = forms.ChoiceField(choices = TRUE_FALSE)
    is_game_organizer.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    is_active = forms.ChoiceField(choices = TRUE_FALSE)
    is_active.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})
    



class UserAddForm(forms.ModelForm):

    TRUE_FALSE = (
        (True, 'Yes'),
        (False, 'No')
    )

    class Meta:
        model = models.User
        fields =["username","contact","wallet","is_game_organizer","is_active",'password']


    username = forms.CharField(max_length=255, label='Enter UserName')
    username.widget.attrs.update({'class': 'form-control','type':'username',"required":"required"})

    contact = forms.CharField(max_length=255, label='Contact Number', required=False)
    contact.widget.attrs.update({'class': 'form-control','type':'number',"required":"required"})

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    wallet = forms.FloatField(initial= 0.0)
    wallet.widget.attrs.update({'class': 'form-control','type':'number',"required":"required"})

    is_game_organizer = forms.ChoiceField(choices = TRUE_FALSE, initial=False)
    is_game_organizer.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    is_active = forms.ChoiceField(choices = TRUE_FALSE)
    is_active.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password Mismatched")
        else:
            hashed_password = make_password(cleaned_data['password'])
            cleaned_data['password'] = hashed_password

        if len(str(cleaned_data['contact']))!= 10:
            raise forms.ValidationError("Enter a ten digit contact number....")
        
        return cleaned_data