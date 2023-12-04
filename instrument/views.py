from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InstrumentForm
from .models import Instrument


class InstrumentCreateView(CreateView):
    model = Instrument
    success_url = '/instruments'
    form_class = InstrumentForm
    template_name = 'instrument_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class InstrumentUpdateView(UpdateView):
    model = Instrument
    success_url = '/instruments'
    form_class = InstrumentForm
    template_name = 'instrument_form.html'


class InstrumentDeleteView(DeleteView):
    model = Instrument
    success_url = '/instruments'
    template_name = 'instrument_delete.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(InstrumentDeleteView, self).post(request, *args, **kwargs)


class InstrumentListView(LoginRequiredMixin, ListView):
    model = Instrument
    context_object_name = "instruments"
    template_name = 'instrument_list.html'
    login_url = "/login"

    def get_queryset(self):
        return Instrument.objects.all().order_by('code')


class InstrumentDetailView(DetailView):
    model = Instrument
    context_object_name = "instrument"
    template_name = 'instrument_details.html'
