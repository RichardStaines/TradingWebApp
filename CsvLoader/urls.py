from django.urls import path
from . import views

urlpatterns = [
    path('csv/load', views.do_form, name='csv.load'),

]
