from django.urls import path
from . import views

urlpatterns = [
    path('ds', views.DividendScheduleListView.as_view(), name='dividend_schedule.list'),
    path('ds/<int:pk>/view', views.DividendScheduleDetailView.as_view(), name='dividend_schedule.details'),
    path('ds/new', views.DividendScheduleCreateView.as_view(), name='dividend_schedule.new'),
    path('ds/<int:pk>/edit', views.DividendScheduleUpdateView.as_view(), name='dividend_schedule.update'),
    path('ds/<int:pk>/delete', views.DividendScheduleDeleteView.as_view(), name='dividend_schedule.delete'),

    path('ds/load', views.csv_load_form, name='dividend_schedule.load'),
    path('ds/scrape', views.scrape_urls_for_ex_div, name='dividend_schedule.scrape_urls_for_ex_div'),

]
