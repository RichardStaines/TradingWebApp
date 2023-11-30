from django.urls import path
from . import views

urlpatterns = [
    path('positions', views.PositionListView.as_view(), name='position.list'),
    path('position/<int:pk>', views.PositionDetailView.as_view(), name='position.details'),
    path('position/new', views.PositionCreateView.as_view(), name='position.new'),
    path('position/<int:pk>/edit', views.PositionUpdateView.as_view(), name='position.update'),
    path('position/<int:pk>/delete', views.PositionDeleteView.as_view(), name='position.delete'),

    path('pos/load', views.csv_load_form, name='position.load'),
    path('positions/yfinance', views.pos_load_from_yfinance, name='positions.loadYfin'),

]
