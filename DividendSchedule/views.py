from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from Tools import LoadCsv
from Utils.ScrapeURL import ScrapeURL
from instrument.models import InstrumentRepository
from .forms import DividendScheduleForm, DividendScheduleCsvLoaderForm
from .models import DividendSchedule, DivScheduleRepository


class DividendScheduleCreateView(CreateView):
    model = DividendSchedule
    success_url = '/ds'
    form_class = DividendScheduleForm
    template_name = 'dividend_schedule_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DividendScheduleUpdateView(UpdateView):
    model = DividendSchedule
    success_url = '/ds'
    form_class = DividendScheduleForm
    template_name = 'dividend_schedule_form.html'


class DividendScheduleDeleteView(DeleteView):
    model = DividendSchedule
    success_url = '/ds'
    context_object_name = "row"
    template_name = 'dividend_schedule_delete.html'


class DividendScheduleListView(LoginRequiredMixin, ListView):
    model = DividendSchedule
    context_object_name = "dividend_schedules"
    template_name = 'dividend_schedule_list.html'
    login_url = "/login"

    def get_queryset(self):
        return DividendSchedule.objects.all().order_by('-payment_date')  # descending order


class DividendScheduleDetailView(DetailView):
    model = DividendSchedule
    context_object_name = "dividend_schedules"
    template_name = 'dividend_schedule_details.html'


def csv_load_form(request):

    # Create a form instance and populate it with data from the request (binding):
    if request.method == 'POST':
        form = DividendScheduleCsvLoaderForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            file_path = form.cleaned_data['file_path']
            clear_before_load = form.cleaned_data['clear_before_load']
            LoadCsv.load_dividend_schedules_from_csv(file_path, clear_before_load)
            pass
    else:
        form = DividendScheduleCsvLoaderForm()
    return render(request, 'ds_csv_loader_form.html', {'form': form})


def scrape_urls_for_ex_div(request):
    instRepo = InstrumentRepository()
    urls_dict = instRepo.get_instruments_for_price_source('yfinance')
    scraper = ScrapeURL()

    for inst_id, instrument in urls_dict.items():
        if instrument['dividend_info_link'] != '':
            ex_div_dict = scraper.get_div(instrument['dividend_info_link'])
            divScheduleRec = DividendSchedule.objects.filter(instrument=inst_id)  # add ex_div_date too
            if len(divScheduleRec) == 0:
                divScheduleRec = DividendSchedule(instrument=instRepo.get_instrument_by_id(inst_id),
                                         payment=0,ex_div_date='10/10/2000')
            else:
                divScheduleRec = divScheduleRec[0]

            # update the record details with the scraped info and save


        #data = update_ticker_history(instrument['price_source_code'], rec=divScheduleRec)

    return HttpResponseRedirect('/ds')