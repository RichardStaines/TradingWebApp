from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PortfolioForm
from .models import Portfolio


class PortfolioCreateView(CreateView):
    model = Portfolio
    success_url = '/portfolios'
    form_class = PortfolioForm
    template_name = 'portfolio_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PortfolioUpdateView(UpdateView):
    model = Portfolio
    success_url = '/portfolios'
    form_class = PortfolioForm
    template_name = 'portfolio_form.html'


class PortfolioDeleteView(DeleteView):
    model = Portfolio
    success_url = '/portfolios'
    template_name = 'portfolio_delete.html'

class PortfolioDetailView(DetailView):
    model = Portfolio
    context_object_name = "portfolio"
    template_name = 'portfolio_details.html'


class PortfolioListView(LoginRequiredMixin, ListView):
    model = Portfolio
    context_object_name = "portfolios"
    template_name = 'portfolio_list.html'
    login_url = "/login"

    def get_queryset(self):
        return Portfolio.objects.all()
        # return self.request.user.portfolio.all()



