import math

from django.db import models

from instrument.models import InstrumentRepository
from portfolio.models import Portfolio


class Cash(models.Model):

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, unique=False, blank=False)
    description = models.CharField(max_length= 100, unique=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    class Meta:
        db_table = "app_cash"


class CashRepository:

    def __init__(self, debug=False):
        self.debug = debug

    def clear_table(self):
        Cash.objects.all().delete()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()

        # print ([f"{row.Type} {row.Datetime} {row.Amount}" for row in df.itertuples()])
        rec_list = [Cash(type=row.Type,
                         description=row.Description,
                         amount=float(row.Amount),
                         payment_date=row.Datetime,
                         portfolio=portfolio
                         ) for row in df.itertuples()]

        if self.debug:
            print(rec_list)
       # print(f"nRows={len(rec_list)}")
        Cash.objects.bulk_create(rec_list, batch_size=len(rec_list))
