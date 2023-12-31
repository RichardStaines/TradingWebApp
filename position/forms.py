from django import forms
from django.core.exceptions import ValidationError

from portfolio.models import Portfolio
from .models import Position


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['portfolio', 'instrument',  'quantity', 'cost', 'avg_price',
                  'pnl','notes',]
        widgets = {
            'portfolio': forms.Select(),
            'instrument': forms.Select(),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),
            'cost': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),
            'avg_price': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),
            'pnl': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),

            'notes': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {'avg_price': 'Average Price (p)',
                  'cost': 'Cost (£)',
                  'pnl': 'PnL (£)'}


class PositionCsvLoaderForm(forms.Form):

    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all())
    file_path = forms.FileField(allow_empty_file=False, required=True)
    clear_before_load = forms.BooleanField(widget=forms.CheckboxInput(), required=False)


