from django import forms
from django.core.exceptions import ValidationError
from .models import Instrument


class InstrumentForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = ['code', 'sedol', 'description', 'price_source']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'sedol': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class':  'form-control'}),
            'price_source': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {'code': 'Code',}

    # the cleaned data is returned by the form
    def clean_code(self):
        code = self.cleaned_data['code']
        if not code[0].isalpha():
            raise ValidationError("Code must start with a letter")
        return code
