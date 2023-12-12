from django.contrib.auth.models import User
from django.db import models


class Instrument(models.Model):

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, blank=False)
    sedol =  models.CharField(max_length =10, unique=False)
    alt_code = models.CharField(max_length=10, unique=False, default='')
    description = models.CharField(max_length=100, unique=False)
    price_source = models.CharField(max_length=20, unique=False)
    price_source_code = models.CharField(max_length=10, default='')
    dividend_info_link = models.URLField(null=False, default='')
    company_link = models.URLField(null=False, default='')
    sector = models.CharField(max_length=20, unique=False, default='')
    dividend_frequency = models.IntegerField(unique=False, default=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    yahoo_chart = ''
    yahoo_info = ''

    class Meta:
        db_table = "app_instrument"
        ordering = ('code',)

    def __str__(self):
        return f"{self.code}"


class InstrumentRepository:

    def __init__(self, debug=True):
        self.debug = debug

    def clear_table(self):
        Instrument.objects.all().delete()

    def get_instrument_by_code(self, code, sedol='', alt_code=''):
        try:
            inst = Instrument.objects.get(code=code)
        except Instrument.DoesNotExist:
            inst = None

        if inst is None and sedol != '':
            try:
                inst = Instrument.objects.get(sedol=sedol)
            except Instrument.DoesNotExist:
                inst = None

        if inst is None and alt_code != '':
            try:
                inst = Instrument.objects.get(alt_code=alt_code)
            except Instrument.DoesNotExist:
                inst = None

        return inst


    def get_instrument_by_id(self, id):
        rec = Instrument.objects.get(pk=id)
        return rec

    def get_instruments_for_price_source(self, price_source):
        qs = Instrument.objects.filter(price_source=price_source).all().values()
        ticker_dict = {rec['id']: rec for rec in qs}
        return ticker_dict


    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        rec_list = [Instrument(code=row.Symbol,
                             sedol=row.Sedol,
                             description=row.Description,
                             ) for row in df.itertuples() if Instrument.objects.get(code=row.Symbol) is None]
        if self.debug:
            print(rec_list)
        if len(rec_list) > 0:
            Instrument.objects.bulk_create(rec_list, batch_size=len(rec_list))
