from django import forms
from django.contrib.auth.hashers import make_password

from . import models

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["username","password",]
    username = forms.CharField(max_length=255, label='UserName')
    username.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter username',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class RegisterForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields =["email","name","password","confirm_password",]

    name = forms.CharField(max_length=255, label='Enter Full Name')
    name.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Full Name',"required":"required"})
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    email = forms.CharField(label='Email')
    email.widget.attrs.update({'class': 'form-control','type':'email', "placeholder":"user@gmail.com","required":"required"})

    

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password Mismatched")
        else:
            hashed_password = make_password(cleaned_data['password'])
            cleaned_data['password'] = hashed_password

        
        return cleaned_data