from django import forms
from main.models import Account


class TransForm(forms.Form):
    user_id = forms.ModelChoiceField(queryset=Account.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))
    balance = forms.CharField(required=True, widget=forms.NumberInput(
        attrs={
            'step': 0.01,
            'class': 'form-control',
            'placeholder': 'Enter balance for transfer'
        }
    ))
    users_to = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter INN of users separated by commas'
        }
    ))
