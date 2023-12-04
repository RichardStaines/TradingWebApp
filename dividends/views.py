from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import ExtractYear
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from portfolio.models import Portfolio, PortfolioRepository
from .forms import DividendForm
from .models import Dividend


class DividendCreateView(CreateView):
    model = Dividend
    success_url = '/dividends'
    form_class = DividendForm
    template_name = 'dividend_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DividendUpdateView(UpdateView):
    model = Dividend
    success_url = '/dividends'
    form_class = DividendForm
    template_name = 'dividend_form.html'


class DividendDeleteView(DeleteView):
    model = Dividend
    success_url = '/dividends'
    template_name = 'dividend_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(DividendDeleteView, self).post(request, *args, **kwargs)

class DividendListView(LoginRequiredMixin, ListView):
    model = Dividend
    context_object_name = "dividends"
    template_name = 'dividends_list.html'
    login_url = "/login"

    def get_context_data(self, *args, **kwargs):
        context = super(DividendListView, self).get_context_data(*args, **kwargs)
        portfolioRepo = PortfolioRepository()
        portfolio_lookup = portfolioRepo.get_portfolio_dict()
        year = datetime.now().year
        years = list(range(year, year-5, -1))
        context['years'] = years
        divs_by_pf_yr = (Dividend.objects.annotate(year=ExtractYear('payment_date'))
                         .values('portfolio','year').annotate(total_amount=Sum('amount'))
                         .order_by('portfolio','-year'))
        div_yr_totals_by_pf = dict()
    #    years = list(set([item['year'] for item in divs_by_pf_yr]))
    #    years.sort(reverse=True)
        pfs = list(set([portfolio_lookup[item['portfolio']] for item in divs_by_pf_yr]))
        pfs.sort()

        portfolio_yr_lookup = {p: {} for p in pfs}
        for item in divs_by_pf_yr:
            p = portfolio_lookup[item['portfolio']]
            y = item['year']
            amount = item['total_amount']
            portfolio_yr_lookup[p][y] = amount

        div_yr_totals_by_pf = []
#        for p in pfs:
#            for y in years:
#                total_amount = portfolio_yr_lookup[p][y] if y in portfolio_yr_lookup[p] else 0
#                yr_totals.append({'total_amount': total_amount})
#            yr_totals = [{'total_amount': portfolio_yr_lookup[p][y] if y in portfolio_yr_lookup[p] else 0}
#                         for y in years]
#            div_yr_totals_by_pf.append( {'portfolio': p, 'byYear': yr_totals} )
        div_yr_totals_by_pf = [{'portfolio': p,
                                'byYear': [{'total_amount':
                                           portfolio_yr_lookup[p][y] if y in portfolio_yr_lookup[p] else 0}
                                           for y in years]}
                               for p in pfs]

        context['portfolios'] = pfs
        context['years'] = years
        context['DividendsByPortfolioYear'] = div_yr_totals_by_pf

        context['DividendsByYear'] = divs_by_pf_yr
        context['DividendsByInstYear'] = (Dividend.objects.annotate(year=ExtractYear('payment_date'))
                                      .values('instrument', 'year').annotate(total_amount=Sum('amount')))
        return context

    def get_queryset(self):
        qs = Dividend.objects.all().annotate(
            payment_year=ExtractYear('payment_date')
        )
        return qs


class DividendDetailView(DetailView):
    model = Dividend
    context_object_name = "dividend"
    template_name = 'dividend_details.html'
