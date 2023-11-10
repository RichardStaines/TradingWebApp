from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CashForm
from .models import Cash


class CashCreateView(CreateView):
    model = Cash
    success_url = '/cash'
    form_class = CashForm
    template_name = 'cash_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CashUpdateView(UpdateView):
    model = Cash
    success_url = '/cash'
    form_class = CashForm
    template_name = 'cash_form.html'


class CashDeleteView(DeleteView):
    model = Cash
    success_url = '/cash'
    template_name = 'cash_delete.html'


class CashListView(LoginRequiredMixin, ListView):
    model = Cash
    context_object_name = "cash_list"
    template_name = 'cash_list.html'
    login_url = "/login"

    def get_queryset(self):
        return Cash.objects.all().order_by('-payment_date')  # descending order


class CashDetailView(DetailView):
    model = Cash
    context_object_name = "cash"
    template_name = 'cash_details.html'
