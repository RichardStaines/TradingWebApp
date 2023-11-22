from django.db.models import Sum
from django.db.models.functions import ExtractYear
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

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


class DividendListView(LoginRequiredMixin, ListView):
    model = Dividend
    context_object_name = "dividends"
    template_name = 'dividends_list.html'
    login_url = "/login"

    def get_context_data(self, *args, **kwargs):
        context = super(DividendListView, self).get_context_data(*args, **kwargs)
        context['DividendsByYear'] = (Dividend.objects.annotate(year=ExtractYear('payment_date'))
                                      .values('year').annotate(total_amount=Sum('amount')).order_by('-year'))
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
