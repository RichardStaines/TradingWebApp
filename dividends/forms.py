from django import forms
from django.core.exceptions import ValidationError
from dividends.models import Dividend


class DividendForm(forms.ModelForm):
    class Meta:
        model = Dividend
        fields = ['portfolio', 'instrument', 'description', 'amount', 'payment_date']
        widgets = {
            'portfolio': forms.Select(),
            'instrument': forms.Select(),
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
        labels = {'instrument': 'Instrument',
                  'payment_date': 'Payment Date'}


