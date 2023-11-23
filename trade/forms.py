from django import forms
from django.core.exceptions import ValidationError
from .models import Trade

BUY_SELL = (
    ('B', 'BUY'),
    ('S', 'SELL'),
)


class TradeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(TradeForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        not_require_list = ['description',]
        for item in not_require_list:
            self.fields[item].required = False

    class Meta:
        model = Trade
        fields = ['portfolio', 'buy_sell', 'instrument',
                  'quantity', 'price', 'net_consideration',
                  'trade_date', 'settle_date', 'description', 'reference'
                  ]
        widgets = {
            'portfolio': forms.Select(),
            'buy_sell': forms.Select(choices=BUY_SELL),
            'instrument': forms.Select(),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),
            'price': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),
            'net_consideration': forms.NumberInput(
                attrs={'class': 'form-control', }
            ),

            'trade_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }
            ),
            'settle_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }
            ),
            'reference':  forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', } ),
        }
        labels = {'payment_date': 'Payment Date'}


