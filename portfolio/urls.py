from django.urls import path, re_path
from . import views

urlpatterns = [
    path('portfolios', views.PortfolioListView.as_view(), name='portfolio.list'),
    path('portfolios/<int:pk>', views.PortfolioDetailView.as_view(), name='portfolio.details'),
    path('portfolios/new', views.PortfolioCreateView.as_view(), name='portfolio.new'),
    path('portfolios/<int:pk>/edit', views.PortfolioUpdateView.as_view(), name='portfolio.update'),
    path('portfolios/<int:pk>/delete', views.PortfolioDeleteView.as_view(), name='portfolio.delete'),

    path('portfolios/load', views.portfolio_csv_load_form, name='portfolio.load'),

    re_path(r'^api/portfolios/$', views.portfolio_list),
    path('api/portfolio/<int:pk>', views.portfolio_detail),
]
