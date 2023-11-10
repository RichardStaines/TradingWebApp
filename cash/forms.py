from django import forms
from django.core.exceptions import ValidationError
from .models import Cash


class CashForm(forms.ModelForm):
    class Meta:
        model = Cash
        fields = ['type', 'description', 'amount', 'payment_date', 'portfolio']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'portfolio': forms.Select(),
            'description': forms.Textarea(attrs={'class':  'form-control'}),
            'amount': forms.NumberInput(
                attrs={'class': 'form-control',}
            ),
            'payment_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }
            ),
        }
        labels = {'payment_date': 'Payment Date'}


