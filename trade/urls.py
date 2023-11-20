from django.urls import path
from . import views

urlpatterns = [
    path('trades', views.TradeListView.as_view(), name='trade.list'),
    path('trades/<str:portfolio>/<str:instrument>', views.TradeListViewByPortfolioInstrument.as_view(),
         name='trade_by_portfolio_and_inst.list'),
    path('trade/<int:pk>', views.TradeDetailView.as_view(), name='trade.details'),
    path('trade/new', views.TradeCreateView.as_view(), name='trade.new'),
    path('trade/<int:pk>/edit', views.TradeUpdateView.as_view(), name='trade.update'),
    path('trade/<int:pk>/delete', views.TradeDeleteView.as_view(), name='trade.delete'),

]
