from django.db import models
from portfolio.models import Portfolio
from instrument.models import Instrument


class Trade(models.Model):

    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=20, unique=False)
    buy_sell = models.CharField(max_length=1, unique=False)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    net_consideration = models.DecimalField(max_digits=12, decimal_places=2)
    trade_date = models.DateField(null=False)
    settle_date = models.DateField(null=False)
    description = models.CharField(max_length=100, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    class Meta:
        db_table = "app_trade"
