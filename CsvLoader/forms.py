from django import forms
from django.core.exceptions import ValidationError
from portfolio.models import Portfolio
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, MultiField, Submit, Div
from crispy_forms.bootstrap import FormActions

class CsvLoaderForm(forms.Form):
#    portfolio = forms.CharField(max_length=20, widget=forms.Select())
    portfolio = forms.ModelChoiceField(queryset=Portfolio.objects.all())
    file_path = forms.FileField(allow_empty_file=False, required=True)
    clear_before_load = forms.BooleanField(widget=forms.CheckboxInput(), required=False)






