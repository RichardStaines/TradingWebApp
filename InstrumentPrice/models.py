from django.contrib.auth.models import User
from django.db import models

from instrument.models import Instrument


# Create your models here.
class InstrumentPrice(models.Model):

    id = models.AutoField(primary_key=True)
    price_source = models.CharField(max_length=20, unique=False)
    open = models.DecimalField(max_digits=12, decimal_places=4)
    close = models.DecimalField(max_digits=12, decimal_places=4)
    high = models.DecimalField(max_digits=12, decimal_places=4)
    low = models.DecimalField(max_digits=12, decimal_places=4)
    volume = models.DecimalField(max_digits=15, decimal_places=0)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    change = models.DecimalField(max_digits=12, decimal_places=4)
    change_percent = models.DecimalField(max_digits=12, decimal_places=4)
    ma50 = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    ma200 = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    year_high = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    year_low = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    pcnt_from_year_high = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    mkt_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.CharField(max_length=4, unique=False, default='')
    exchange = models.CharField(max_length=6, unique=False, default='')

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "app_instrument_price"

    def __str__(self):
        return f"{self.instrument}"
