from django import forms
from django.core.exceptions import ValidationError
from DividendSchedule.models import DividendSchedule
from instrument.models import Instrument


class DividendScheduleForm(forms.ModelForm):
    class Meta:
        model = DividendSchedule
        fields = ['instrument', 'payment', 'ex_div_date', 'payment_date', ]
        widgets = {
            'instrument': forms.Select(),
            'payment': forms.NumberInput(
                attrs={'class': 'form-control',}
            ),
            'ex_div_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }
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
                  'payment_date': 'Payment Date',
                  }


class DividendScheduleCsvLoaderForm(forms.Form):

    file_path = forms.FileField(allow_empty_file=False, required=True)
    clear_before_load = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
