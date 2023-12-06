import decimal

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from instrument.models import InstrumentRepository
from .forms import InstrumentPriceForm
from .models import InstrumentPrice
import pandas as pd
import yfinance as yf
import yfinance.shared as share


class InstrumentPriceCreateView(CreateView):
    model = InstrumentPrice
    success_url = '/prices/instrument_prices'
    form_class = InstrumentPriceForm
    template_name = 'instrument_price_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class InstrumentPriceUpdateView(UpdateView):
    model = InstrumentPrice
    success_url = '/prices/instrument_prices'
    form_class = InstrumentPriceForm
    template_name = 'instrument_price_form.html'


class InstrumentPriceDeleteView(DeleteView):
    model = InstrumentPrice
    context_object_name = "instrument_price"
    success_url = '/prices/instrument_prices'
    template_name = 'instrument_price_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(InstrumentPriceDeleteView, self).post(request, *args, **kwargs)


class InstrumentPriceListView(LoginRequiredMixin, ListView):
    model = InstrumentPrice
    context_object_name = "instrument_prices"
    template_name = 'instrument_price_list.html'
    login_url = "/login"

    def get_queryset(self):
        return InstrumentPrice.objects.select_related('instrument').all().order_by('instrument')


class InstrumentPriceDetailView(DetailView):
    model = InstrumentPrice
    context_object_name = "instrument_price"
    template_name = 'instrument_price_details.html'


def get_ticker_history(_ticker, _start_date=None, _end_date=None, _interval='1min', _period='1h', ip_rec=None):
    print(_ticker)
    _ticker = _ticker.strip()
    ticker_data = yf.Ticker(_ticker, session=None).fast_info
    if ip_rec is not None:
        ip_rec.price_source = 'yfinance'
        ip_rec.close = ticker_data.previous_close
        ip_rec.open = ticker_data.open
        ip_rec.volume = ticker_data.last_volume
        ip_rec.price = ticker_data.last_price
        ip_rec.high = ticker_data.day_high
        ip_rec.low = ticker_data.day_low
        ip_rec.year_high = ticker_data.year_high
        ip_rec.year_low = ticker_data.year_low
        ip_rec.change = ip_rec.price - ip_rec.close
        ip_rec.change_percent = 100 * (ip_rec.change / ip_rec.close)
        ip_rec.ma50 = ticker_data.fifty_day_average
        ip_rec.ma200 = ticker_data.two_hundred_day_average
        ip_rec.mkt_cap = ticker_data.market_cap
        ip_rec.exchange = ticker_data.exchange
        ip_rec.currency = ticker_data.currency
        ip_rec.pcnt_from_year_high = 100 * (ticker_data.year_high - ticker_data.last_price) / ticker_data.last_price
        ip_rec.save()

    return ticker_data


def load_from_yfinance_and_reload(request, reload_url):
    # get list of RICs
    instRepo = InstrumentRepository()
    tickers_dict= instRepo.get_instruments_for_price_source('yfinance')

    yf.pdr_override()  # <== that's all it takes :-)
    for inst_id, instrument in tickers_dict.items():
        ipRec = InstrumentPrice.objects.filter(instrument=inst_id)
        if len(ipRec) == 0:
            ipRec = InstrumentPrice(instrument=instRepo.get_instrument_by_id(inst_id), open=0, close=0, price=0)
        else:
            ipRec = ipRec[0]
        # update record with instrument price data
        data = get_ticker_history(instrument['price_source_code'], ip_rec=ipRec)

    return HttpResponseRedirect(reload_url)


def load_from_yfinance(request):
    return load_from_yfinance_and_reload(request, '/prices/instrument_prices')