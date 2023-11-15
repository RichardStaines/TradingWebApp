from django.db import models
from portfolio.models import Portfolio
from instrument.models import Instrument, InstrumentRepository


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


class DividendRepository:

    def __init__(self, debug=False):
        self.debug = debug

    def clear_table(self):
        Dividend.objects.all().delete()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        instRepo = InstrumentRepository()
        rec_list = [Dividend(instrument=instRepo.get_instrument_by_code(div.Symbol),
                             sedol=div.Sedol,
                             description=div.Description,
                             amount=div.Credit,
                             payment_date=div.Datetime,
                             portfolio=portfolio
                             ) for div in df.itertuples()]
        if self.debug:
            print(rec_list)
        Dividend.objects.bulk_create(rec_list, batch_size=len(rec_list))