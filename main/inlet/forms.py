from django import forms
from .models import ProductIndex

class ProductIndexForm(forms.ModelForm):
    class Meta:
        model = ProductIndex
        fields = '__all__'  