from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from CsvLoader.forms import CsvLoaderForm

from Tools import LoadCsv

def do_form(request):

    # Create a form instance and populate it with data from the request (binding):
    if request.method == 'POST':
        form = CsvLoaderForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            portfolio_name = form.cleaned_data['portfolio']
            file_path = form.cleaned_data['file_path']
            clear_before_load = form.cleaned_data['clear_before_load']
            LoadCsv.load_from_csv(portfolio_name, file_path, clear_before_load)
            pass
    else:
        form = CsvLoaderForm()
    return render(request, 'csv_loader_form.html', {'form': form})


# Create your views here.
class CsvLoadView:
    template_name = 'csv_loader_form.html'

    @staticmethod
    def do_form(request):
        form = CsvLoaderForm()
        form.render()
        context = {
            'form': form,
        }
        return render(request, 'csv_loader_form.html', context)

