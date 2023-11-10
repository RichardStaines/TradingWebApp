from django.urls import path
from . import views

urlpatterns = [
    path('instruments', views.InstrumentListView.as_view(), name='instrument.list'),
    path('instrument/<int:pk>', views.InstrumentDetailView.as_view(), name='instrument.details'),
    path('instrument/new', views.InstrumentCreateView.as_view(), name='instrument.new'),
    path('instrument/<int:pk>/edit', views.InstrumentUpdateView.as_view(), name='instrument.update'),
    path('instrument/<int:pk>/delete', views.InstrumentDeleteView.as_view(), name='instrument.delete'),
]
