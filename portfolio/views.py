from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from Tools import LoadCsv
from .forms import PortfolioForm, PortfolioCsvLoadForm
from .models import Portfolio


class PortfolioCreateView(CreateView):
    model = Portfolio
    success_url = '/portfolios'
    form_class = PortfolioForm
    template_name = 'portfolio_csv_load_form.html'

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
        return Portfolio.objects.all().order_by('name')
        # return self.request.user.portfolio.all()


def portfolio_csv_load_form(request):

    # Create a form instance and populate it with data from the request (binding):
    if request.method == 'POST':
        form = PortfolioCsvLoadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data (e.g., send an email)
            file_path = form.cleaned_data['file_path']
            clear_before_load = form.cleaned_data['clear_before_load']
            LoadCsv.load_portfolios_csv(file_path, clear_before_load)
            return redirect('portfolio.list')
    else:
        form = PortfolioCsvLoadForm()
    return render(request, 'portfolio_csv_loader_form.html', {'form': form})

