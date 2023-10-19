from django import forms
from .models import SaleOrder, SaleOrderProduct

class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = '__all__'

class SaleOrderProductForm(forms.ModelForm):
    class Meta:
        model = SaleOrderProduct
        fields = '__all__'


class AddUUIDForm(forms.Form):
    text_input = forms.CharField(max_length=100, required=False)