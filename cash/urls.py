from django.urls import path
from . import views

urlpatterns = [
    path('cash', views.CashListView.as_view(), name='cash.list'),
    path('cash/<int:pk>', views.CashDetailView.as_view(), name='cash.details'),
    path('cash/new', views.CashCreateView.as_view(), name='cash.new'),
    path('cash/<int:pk>/edit', views.CashUpdateView.as_view(), name='cash.update'),
    path('cash/<int:pk>/delete', views.CashDeleteView.as_view(), name='cash.delete'),
]
