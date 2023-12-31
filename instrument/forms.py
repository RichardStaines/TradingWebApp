from django import forms
from django.core.exceptions import ValidationError
from .models import Instrument


class InstrumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(InstrumentForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        not_mandatory_list = ['price_source_code', 'price_source',
                              'sedol', 'alt_code', 'dividend_info_link', 'company_link',
                              'sector', 'dividend_frequency'
                              ]
        for item in not_mandatory_list:
            self.fields[item].required = False

    class Meta:
        model = Instrument
        fields = ['code', 'sedol', 'alt_code', 'description',
                  'price_source', 'price_source_code',
                  'dividend_info_link', 'company_link',
                  'sector', 'dividend_frequency']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'sedol': forms.TextInput(attrs={'class': 'form-control'}),
            'alt_code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class':  'form-control'}),
            'price_source': forms.TextInput(attrs={'class': 'form-control'}),
            'price_source_code': forms.TextInput(attrs={'class': 'form-control'}),
            'dividend_info_link': forms.TextInput(attrs={'class': 'form-control'}),
            'company_link': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'dividend_frequency': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {'code': 'Code',
                  'dividend_info_link': 'Dividend Info Link (a source of dividend information)',
                  'dividend_frequency': 'Divs Per Yr',
                  }

    # the cleaned data is returned by the form
    def clean_code(self):
        code = self.cleaned_data['code']
        if not code[0].isalpha():
            raise ValidationError("Code must start with a letter")
        return code
