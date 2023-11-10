from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class TradeDetailView(DetailView):
    model = Trade
    context_object_name = "trades"
    template_name = 'trade_details.html'
