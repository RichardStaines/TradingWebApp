from django.urls import path
from . import views

urlpatterns = [
    path('portfolios', views.PortfolioListView.as_view(), name='portfolio.list'),
    path('portfolios/<int:pk>', views.PortfolioDetailView.as_view(), name='portfolio.details'),
    path('portfolios/new', views.PortfolioCreateView.as_view(), name='portfolio.new'),
    path('portfolios/<int:pk>/edit', views.PortfolioUpdateView.as_view(), name='portfolio.update'),
    path('portfolios/<int:pk>/delete', views.PortfolioDeleteView.as_view(), name='portfolio.delete'),
]
