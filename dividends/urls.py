from django.urls import path
from . import views

urlpatterns = [
    path('dividends', views.DividendListView.as_view(), name='dividend.list'),
    path('dividend/<int:pk>', views.DividendDetailView.as_view(), name='dividend.details'),
    path('dividend/new', views.DividendCreateView.as_view(), name='dividend.new'),
    path('dividend/<int:pk>/edit', views.DividendUpdateView.as_view(), name='dividend.update'),
    path('dividend/<int:pk>/delete', views.DividendDeleteView.as_view(), name='dividend.delete'),
]
