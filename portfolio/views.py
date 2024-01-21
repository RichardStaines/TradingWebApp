from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from Tools import LoadCsv
from .forms import PortfolioForm, PortfolioCsvLoadForm
from .models import Portfolio
from .serializers import *


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

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.success_url
            return HttpResponseRedirect(url)
        else:
            return super(PortfolioDeleteView, self).post(request, *args, **kwargs)


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


@api_view(['GET', 'POST'])
def portfolio_list(request):
    if request.method == 'GET':
        data = Portfolio.objects.all()
        serializer = PortfolioSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def portfolio_detail(request, pk):
    try:
        portfolio = Portfolio.objects.get(id=pk)
    except Portfolio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PortfolioSerializer(portfolio, context={'request': request}, many=False)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = PortfolioSerializer(portfolio, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
