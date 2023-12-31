from django.contrib.auth.models import User
from django.db import models

from InstrumentPrice.models import InstrumentPrice
from portfolio.models import Portfolio
from instrument.models import Instrument, InstrumentRepository
from trade.models import Trade


class Position(models.Model):

    id = models.AutoField(primary_key=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=0)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    avg_price = models.DecimalField(max_digits=12, decimal_places=2)
    pnl = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.CharField(max_length=100, unique=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    div_payment_per_share = 0
    div_payment_per_share_pcnt = 0  # pcnt of mkt price
    div_payment_per_share_pcnt_of_cost = 0
    div_ytd = 0
    div_ytd_pcnt_of_cost = 0
    div_last = 0
    div_prev = 0
    year = 0
    position_value = 0
    value_change = 0
    unrealised_pnl = 0
    unrealised_pnl_pct = 0 # as %age of cost
    instrument_price = None # manual join to instrument price table
    dividend_schedule = None

    class Meta:
        db_table = "app_position"
        unique_together = [["portfolio", "instrument"]]
        indexes = [
            models.Index(fields=["portfolio", "instrument"]),
        ]


class PositionRepository:

    def __init__(self, debug=False):
        self.debug = debug

    def update_position_with_trade(self, trade: Trade, user, mode="NEW"):
        """
        Adjust the position by the effects of the trade
        :param trade: trade object
        :param user: user entering the trade
        :param mode: NEW or CANCEL
        :return: the pnl for the trade when sell, 0 when buy
        """
        trade_pnl = 0
        notes_suffix = f" by TradeId {trade.reference} {trade.buy_sell} {trade.quantity}@{trade.price}"
        qs = Position.objects.filter(portfolio=trade.portfolio, instrument=trade.instrument)
        if len(qs) == 0:
            # create a new position for the trade
            pos = Position(portfolio=trade.portfolio, instrument=trade.instrument,
                           quantity=trade.quantity, avg_price=trade.price,
                           cost=trade.net_consideration, notes=f"Created {notes_suffix}")
        elif trade.buy_sell == 'S':
            # sell trades don't affect avg_price they affect PnL
            pos = qs[0]
            trade_pnl = (trade.net_consideration - (trade.quantity * pos.avg_price / 100))
            if mode == "NEW":
                pos.quantity -= trade.quantity
                pos.pnl += trade_pnl
            else:
                pos.quantity += trade.quantity
                pos.pnl -= trade_pnl

                # pos.cost -= trade.net_consideration
            pos.cost = ( pos.quantity * pos.avg_price) / 100
            pos.notes = f"Updated {notes_suffix}"
        else:
            pos = qs[0]
            if mode == "NEW":
                pos.quantity += trade.quantity
                pos.cost += trade.net_consideration
            else:
                pos.quantity -= trade.quantity
                pos.cost -= trade.net_consideration
            new_avg_price = (pos.cost / pos.quantity) if pos.quantity != 0 else 0
            pos.avg_price = new_avg_price * 100
            pos.notes = f"Updated {notes_suffix}"
        pos.save()
        return trade_pnl

    def clear_table(self):
        Position.objects.all().delete()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()

        cols = df.columns
        instRepo = InstrumentRepository()
        x = [pos for pos in df.itertuples()]
        print (x)
        rec_list = [Position(instrument=instRepo.get_instrument_by_code(pos.Symbol),
                             quantity=pos.Qty,
                             avg_price=pos.AvgPrice,
                             cost=pos.Cost,
                             portfolio=portfolio
                          ) for pos in df.itertuples()]
        if self.debug:
            print(rec_list)
        Position.objects.bulk_create(rec_list, batch_size=len(rec_list))


