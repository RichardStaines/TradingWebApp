from django.urls import path
from . import views

urlpatterns = [
    path('instrument_prices', views.InstrumentPriceListView.as_view(), name='instrument_price.list'),
    path('instrument_price/<int:pk>', views.InstrumentPriceDetailView.as_view(), name='instrument_price.details'),
    path('instrument_price/new', views.InstrumentPriceCreateView.as_view(), name='instrument_price.new'),
    path('instrument_price/<int:pk>/edit', views.InstrumentPriceUpdateView.as_view(), name='instrument_price.update'),
    path('instrument_price/<int:pk>/delete', views.InstrumentPriceDeleteView.as_view(), name='instrument_price.delete'),
]
