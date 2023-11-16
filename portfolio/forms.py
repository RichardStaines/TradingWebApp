from django import forms
from django.core.exceptions import ValidationError
from portfolio.models import Portfolio


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control my-5'}),
            'description': forms.Textarea(attrs={'class':  'form-control mb-5'}),
        }
        labels = {'name': 'Name',
                  'description': 'Description'}

    # the cleaned data is returned by the form
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name[0].isalpha():
            raise ValidationError("Name must start with a letter")
        return name


class PortfolioCsvLoadForm(forms.Form):

    file_path = forms.FileField(allow_empty_file=False, required=True)
    clear_before_load = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

