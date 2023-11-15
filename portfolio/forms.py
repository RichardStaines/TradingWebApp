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


class PortfolioCsvLoadForm(forms.ModelForm):
    # template_name = 'portfolio_csv_load_form.html'

    def __int__(self, user=None, *args, **kwargs):
        super(PortfolioCsvLoadForm, self).__init__(*args, **kwargs)
        self.fields["templates"] =  {
            'file_path': forms.TextInput(attrs={'class': 'form-control'}),
            'clear_before_load': forms.CheckboxInput(attrs={'class': 'required checkbox form-control'}),
        }

    class Meta:
        model = Portfolio
        fields = []
        widgets = {
            'file_path': forms.TextInput(attrs={'class': 'form-control'}),
            'clear_before_load': forms.CheckboxInput(attrs={'class': 'required checkbox form-control'}),
        }
        labels = {'clear_before_load': 'Clear Before Load'}

