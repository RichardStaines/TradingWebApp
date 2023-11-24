from django.db import models
from portfolio.models import Portfolio
from instrument.models import Instrument, InstrumentRepository
from django.contrib.auth.models import User


class Trade(models.Model):

    id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=20, unique=False)
    buy_sell = models.CharField(max_length=1, unique=False)
    quantity = models.DecimalField(max_digits=12, decimal_places=0)
    price = models.DecimalField(max_digits=12, decimal_places=6)
    net_consideration = models.DecimalField(max_digits=12, decimal_places=2)
    trade_date = models.DateField(null=False)
    settle_date = models.DateField(null=False)
    description = models.CharField(max_length=100, unique=False)
    pnl = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "app_trade"


class TradeRepository:

    def __init__(self, debug=False):
        self.debug = debug

    def clear_table(self):
        Trade.objects.all().delete()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        instRepo = InstrumentRepository()
        rec_list = [Trade(instrument=instRepo.get_instrument_by_code(trd.Symbol),
                          buy_sell=trd.BuySell,
                          quantity=trd.Quantity,
                          price=trd.Price,
                          net_consideration=trd.Consideration,
                          trade_date=trd.Datetime,
                          reference=trd.Reference,
                          settle_date=trd.SettleDate,
                          portfolio=portfolio
                          ) for trd in df.itertuples()]
        if self.debug:
            print(rec_list)
        Trade.objects.bulk_create(rec_list, batch_size=len(rec_list))


