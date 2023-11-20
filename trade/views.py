from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from instrument.models import InstrumentRepository
from portfolio.models import PortfolioRepository
from .forms import TradeForm
from .models import Trade


class TradeCreateView(CreateView):
    model = Trade
    success_url = '/trades'
    form_class = TradeForm
    template_name = 'trade_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TradeUpdateView(UpdateView):
    model = Trade
    success_url = '/trades'
    form_class = TradeForm
    template_name = 'trade_form.html'


class TradeDeleteView(DeleteView):
    model = Trade
    success_url = '/trades'
    template_name = 'trade_delete.html'


class TradeListView(LoginRequiredMixin, ListView):
    model = Trade
    context_object_name = "trades"
    template_name = 'trade_list.html'
    login_url = "/login"

    def get_queryset(self):
        return Trade.objects.all().order_by('-trade_date')  # descending order


class TradeListViewByPortfolioInstrument(LoginRequiredMixin, ListView):
    model = Trade
    context_object_name = "trades"
    template_name = 'trade_list.html'
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = {
            'extra_title' : f"for position {self.portfolio_name} {self.instrument_code}"
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.portfolio_name = self.kwargs.get('portfolio')
        portRepo = PortfolioRepository()
        portfolio_id = portRepo.get_portfolio(self.portfolio_name).id
        self.instrument_code = self.kwargs.get('instrument')
        instRepo = InstrumentRepository()
        inst_id = instRepo.get_instrument_by_code(self.instrument_code).id
        return (Trade.objects.all().filter(portfolio=portfolio_id, instrument=inst_id)
                .order_by('-trade_date'))  # descending order


class TradeDetailView(DetailView):
    model = Trade
    context_object_name = "trades"
    template_name = 'trade_details.html'
