from django.db import models

from instrument.models import Instrument, InstrumentRepository


# Create your models here.
class DividendSchedule( models.Model):

    id = models.AutoField(primary_key=True)
    # instrument = models.CharField(max_length=10, unique=False, blank=False)
    payment = models.DecimalField(max_digits=12, decimal_places=2)
    ex_div_date = models.DateField(null=False)
    payment_date = models.DateField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)


class DivScheduleRepository:

    def __init__(self, debug=True):
        self.debug = debug

    def clear_table(self):
        DividendSchedule.objects.all().delete()

    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        instRepo = InstrumentRepository()
        rec_list = [DividendSchedule(ex_div_date=row.ex_div_date,
                                     payment_date=row.payment_date,
                                     payment=row.payment,
                                     instrument=instRepo.get_instrument_by_code(row.Symbol)
                             ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        DividendSchedule.objects.bulk_create(rec_list, batch_size=len(rec_list))
