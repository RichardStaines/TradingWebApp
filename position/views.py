from django.db.models.expressions import RawSQL
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DateField, CharField, Value, Window, F, Max, ExpressionWrapper, QuerySet

from DividendSchedule.models import DividendSchedule
from Tools import LoadCsv
from trade.models import Trade
from .forms import PositionForm, PositionCsvLoaderForm
from .models import Position


class PositionCreateView(CreateView):
    model = Position
    success_url = '/pos/positions'
    form_class = PositionForm
    template_name = 'position_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PositionUpdateView(UpdateView):
    model = Position
    success_url = '/pos/positions'
    form_class = PositionForm
    template_name = 'position_form.html'


class PositionDeleteView(DeleteView):
    model = Position
    success_url = '/pos/positions'
    template_name = 'position_delete.html'


class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    context_object_name = "positions"
    template_name = 'position_list.html'
    login_url = "/login"

    def get_queryset(self):
        qs = Position.objects.all()
      #  instruments = [item.instrument.id for item in qs]
      #  ds_qs = (DividendSchedule.objects
      #           .filter(instrument__in=instruments)
      #           )
      #  ex_div_lookup = {item.instrument.id: item.ex_div_date for item in ds_qs}

        qs = qs.annotate(ex_div_date=RawSQL("select max(ex_div_date) as ex_div_date "
                                             "from app_dividendschedule "
                                             "where instrument_id = app_position.instrument_id "
                                             "GROUP by instrument_id", []),
                      )
        return qs

    # + Value(ex_div_lookup.get(551) )


class PositionDetailView(DetailView):
    model = Position
    context_object_name = "position"
    template_name = 'position_details.html'


def csv_load_form(request):
    # Create a form instance and populate it with data from the request (binding):
    if request.method == 'POST':
        form = PositionCsvLoaderForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            portfolio = form.cleaned_data['portfolio']
            file_path = form.cleaned_data['file_path']
            clear_before_load = form.cleaned_data['clear_before_load']
            LoadCsv.load_positions_from_csv(portfolio, file_path, clear_before_load)
            pass
    else:
        form = PositionCsvLoaderForm()
    return render(request, 'pos_csv_loader_form.html', {'form': form})
