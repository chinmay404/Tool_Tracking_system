# forms.py
from django import forms

class ActivationForm(forms.Form):
    id = forms.UUIDField(label='Enter ID', widget=forms.TextInput(attrs={'placeholder': 'Enter ID'}))
