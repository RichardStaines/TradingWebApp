from django.db import models
from portfolio.models import Portfolio
from instrument.models import Instrument


class Dividend( models.Model):

    id = models.AutoField(primary_key=True)
    # instrument = models.CharField(max_length=10, unique=False, blank=False)
    sedol =  models.CharField(max_length =10, unique=False)
    description = models.CharField(max_length= 100, unique=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    class Meta:
        db_table = "app_dividend"
