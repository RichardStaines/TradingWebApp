from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InstrumentPriceForm
from .models import InstrumentPrice


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
    success_url = '/prices/instrument_prices'
    template_name = 'instrument_price_delete.html'


class InstrumentPriceListView(LoginRequiredMixin, ListView):
    model = InstrumentPrice
    context_object_name = "instrument_prices"
    template_name = 'instrument_price_list.html'
    login_url = "/login"

    def get_queryset(self):
        return InstrumentPrice.objects.all().order_by('instrument')


class InstrumentPriceDetailView(DetailView):
    model = InstrumentPrice
    context_object_name = "instrument_price"
    template_name = 'instrument_price_details.html'
