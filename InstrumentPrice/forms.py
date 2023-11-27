from django import forms
from django.core.exceptions import ValidationError
from .models import InstrumentPrice


class InstrumentPriceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(InstrumentPriceForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        not_require_list = ['price_source', 'open', 'high', 'low', 'change', 'change_percent', 'volume']
        for item in not_require_list:
            self.fields[item].required = False

    class Meta:
        model = InstrumentPrice
        fields = ['instrument', 'price_source',
                  'open', 'close', 'high', 'low',
                  'volume', 'price', 'change', 'change_percent'
                  ]
        widgets = {
            'instrument': forms.Select(),
            'price_source': forms.TextInput(attrs={'class': 'form-control'}),
            'open': forms.NumberInput(attrs={'class': 'form-control', }),
            'close': forms.NumberInput(attrs={'class': 'form-control', }),
            'high': forms.NumberInput(attrs={'class': 'form-control', }),
            'low': forms.NumberInput(attrs={'class': 'form-control', }),
            'volume': forms.NumberInput(attrs={'class': 'form-control', }),
            'price': forms.NumberInput(attrs={'class': 'form-control', }),
            'change': forms.NumberInput(attrs={'class': 'form-control', }),
            'change_percent': forms.NumberInput(attrs={'class': 'form-control', }),
        }
        labels = {'instrument': 'Instrument',
                  }


