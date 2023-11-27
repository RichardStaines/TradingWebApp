import decimal
from datetime import datetime

from django.db.models.expressions import RawSQL
from django.db.models.functions import ExtractYear
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import DateField, CharField, Value, Window, F, Max, ExpressionWrapper, QuerySet, Sum

from DividendSchedule.models import DividendSchedule
from InstrumentPrice.models import InstrumentPrice
from Tools import LoadCsv
from dividends.models import Dividend, DividendRepository
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

    def get_context_data(self, *args, **kwargs):
        context = super(PositionListView, self).get_context_data(*args, **kwargs)
        context['year'] = datetime.now().year
        context['last_year'] = datetime.now().year - 1
        context['prev_year'] = datetime.now().year - 2

        return context

    def get_queryset(self):
        qs = Position.objects.all()
#        qs_dict_list = [model_to_dict(item) for item in qs]
#        instruments = [item.instrument.id for item in qs]
#        ds_qs = (DividendSchedule.object.filter(instrument__in=instruments)
#                )
#        ds_qs = (DividendSchedule.objects.values('instrument_id')
#                 .annotate(ex_div_date=Max('ex_div_date'))
#                 )
        divRepo = DividendRepository()
        divRepo.get_dividends_by_inst_year()

        ds_qs = (DividendSchedule.objects.all().order_by('ex_div_date').values()
                 )
        ex_div_lookup = {item['instrument_id']: item for item in ds_qs}

        ip_qs = InstrumentPrice.objects.all().values()
        price_lookup = {item['instrument_id']: item for item in ip_qs}
        new_qs = []
        for item in qs:
            item.year,item.div_ytd = divRepo.get_dividend_total(item.portfolio_id, item.instrument_id, "YTD")
            _,item.div_last = divRepo.get_dividend_total(item.portfolio_id, item.instrument_id, "LAST")
            _,item.div_prev = divRepo.get_dividend_total(item.portfolio_id, item.instrument_id, "PREV")
            item.ex_div_date = ex_div_lookup[item.instrument_id]['ex_div_date'] \
                if item.instrument_id in ex_div_lookup else ''
            item.payment_date = ex_div_lookup[item.instrument_id]['payment_date'] \
                if item.instrument_id in ex_div_lookup else ''
            item.div_payment_per_share = ex_div_lookup[item.instrument_id]['payment'] if item.instrument_id in ex_div_lookup else 0

            item.mkt_price = price_lookup[item.instrument_id]['price'] \
                if item.instrument_id in price_lookup else ''
            item.change = price_lookup[item.instrument_id]['change'] \
                if item.instrument_id in price_lookup else ''
            item.change_pct = price_lookup[item.instrument_id]['change_percent'] \
                if item.instrument_id in price_lookup else ''
            item.position_value = (decimal.Decimal(item.mkt_price) * item.quantity) / 100 if item.mkt_price != '' else 0
            item.unrealised_pnl = item.position_value - item.cost
            new_qs.append(item)

        #qs = qs.annotate(ex_div_date2=RawSQL("select max(ex_div_date) as ex_div_date "
        #                                     "from app_dividendschedule "
        #                                     "where instrument_id = app_position.instrument_id "
        #                                     "GROUP by instrument_id", []),
        #              )

        return new_qs

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
