from django.db import models
from django.db.models import Sum
from django.db.models.functions import ExtractYear

from portfolio.models import Portfolio
from instrument.models import Instrument, InstrumentRepository
from datetime import datetime


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

    @staticmethod
    def format_inst_year_key(instrument_id, year):
        return f"{instrument_id}-{year}"

    def get_inst_year(self):
        return Dividend.format_inst_year_key(self.instrument_id, self.payment_date.year)


class DividendRepository:

    def __init__(self, debug=False):
        self.debug = debug
        self.get_dividends_by_inst_year()

    def clear_table(self):
        Dividend.objects.all().delete()


    def get_dividends_by_inst_year(self):
        self.divs_qs = (Dividend.objects.annotate(year=ExtractYear('payment_date'))
                                          .values('instrument_id', 'year').annotate(total_amount=Sum('amount')))
        # convert to dict
        self.div_year_lookup = {Dividend.format_inst_year_key(div['instrument_id'], div['year'])
                                : div['total_amount'] for div in self.divs_qs}
        return self.div_year_lookup

    def get_dividend_total(self, instrument_id, year_code="YTD"):
        year = datetime.now().year
        if year_code == 'LAST':
            year = year - 1
        elif year_code == 'PREV':
            year = year - 2
        key = Dividend.format_inst_year_key(instrument_id, year)
        return (year,self.div_year_lookup[key] if key in self.div_year_lookup else 0)

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