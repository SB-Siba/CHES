from django import forms
from app_common.models import Order,ProduceBuy

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'order_status',
        ]
    
    order_status = forms.ChoiceField(choices = Order.ORDER_STATUS)
    order_status.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

class ProduceOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = ProduceBuy
        fields = [
            'buying_status',
        ]
    
    buying_status = forms.ChoiceField(choices = ProduceBuy.BUYINGSTATUS)
    buying_status.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})