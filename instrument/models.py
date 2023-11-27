from django.contrib.auth.models import User
from django.db import models


class Instrument(models.Model):

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, blank=False)
    sedol =  models.CharField(max_length =10, unique=False)
    description = models.CharField(max_length=100, unique=False)
    price_source = models.CharField(max_length=20, unique=False)
    price_source_code = models.CharField(max_length=10, default='')
    dividend_info_link = models.URLField(null=False, default='')
    company_link = models.URLField(null=False, default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "app_instrument"

    def __str__(self):
        return f"{self.code}"


class InstrumentRepository:

    def __init__(self, debug=True):
        self.debug = debug

    def clear_table(self):
        Instrument.objects.all().delete()

    def get_instrument_by_code(self, code):
        qs = Instrument.objects.filter(code=code)
        return qs[0] if len(qs) > 0 else None

    def get_instruments_for_price_source(price_source):
        return Instrument.query.filter_by(price_source=price_source).all()

    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        rec_list = [Instrument(code=row.Symbol,
                             sedol=row.Sedol,
                             description=row.Description,
                             ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        Instrument.objects.bulk_create(rec_list, batch_size=len(rec_list))
