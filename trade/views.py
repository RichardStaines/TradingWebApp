from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from instrument.models import InstrumentRepository
from portfolio.models import PortfolioRepository
from position.models import PositionRepository
from .forms import TradeForm
from .models import Trade


class TradeCreateView(CreateView):
    model = Trade
    success_url = '/trades'
    form_class = TradeForm
    template_name = 'trade_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TradeCreateView, self).get_context_data(*args, **kwargs)
        context['mode'] = 'Entry'

        return context

    def form_valid(self, form):
        if form.instance.price is None or form.instance.price == 0:
            form.instance.price = (form.instance.net_consideration / form.instance.quantity)
        self.object = form.save(commit=False)
        posRepo = PositionRepository()
        self.object.pnl = posRepo.update_position_with_trade(self.object, self.request.user)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TradeUpdateView(UpdateView):
    model = Trade
    success_url = '/trades'
    form_class = TradeForm
    template_name = 'trade_form.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TradeUpdateView, self).get_context_data(*args, **kwargs)
        context['mode'] = 'Update'
        return context

    def form_valid(self, form):
        if form.instance.price is None or form.instance.price == 0:
            form.instance.price = (form.instance.net_consideration / form.instance.quantity)
        self.object = form.save(commit=False)
        posRepo = PositionRepository()
        pre_amended_trade = Trade.objects.get(pk=self.object.id)
        if ((pre_amended_trade.price != self.object.price) or (pre_amended_trade.quantity != self.object.quantity)
                or pre_amended_trade.net_consideration != self.object.net_consideration):
            posRepo.update_position_with_trade(pre_amended_trade, self.request.user, 'CANCEL')
            self.object.pnl = posRepo.update_position_with_trade(self.object, self.request.user, 'NEW')
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class TradeDeleteView(DeleteView):
    model = Trade
    success_url = '/trades'
    template_name = 'trade_delete.html'

    def form_valid(self, form):
        posRepo = PositionRepository()
        self.object.pnl = posRepo.update_position_with_trade(self.object, self.request.user, "CANCEL")
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(TradeDeleteView, self).post(request, *args, **kwargs)



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
