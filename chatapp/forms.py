from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {'content': ''}

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Message',
            'rows': 1,
            'required': 'required'
        })