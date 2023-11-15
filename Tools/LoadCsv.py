import sys
import os
import argparse

from cash.models import *
from dividends.models import *
from trade.models import *
from Utils.iiCSV import IICsv
from portfolio.models import *
from instrument.models import  *


def load_from_csv(portfolio, filename, clear_before_load):

    #portfolio_repo = PortfolioRepository()
    #portfolio = portfolio_repo.get_portfolio(portfolio_name)
    #if portfolio is None:
    #    return f"portfolio:{portfolio_name} is not registered"

    ii_csv = IICsv(filename, debug=True)

    instRepo = InstrumentRepository()
    cashRepo = CashRepository()
    divRepo = DividendRepository()
    tradeRepo = TradeRepository()

    print(f"Instruments={ii_csv.get_instruments()}")
    instRepo.save_from_df(ii_csv.get_instruments(), clear_before_load)

    divRepo.save_from_df(ii_csv.get_dividends(), portfolio, clear_before_load)
    tradeRepo.save_from_df(ii_csv.get_trades(), portfolio, clear_before_load)
    cashRepo.save_from_df(ii_csv.get_cash(), portfolio, clear_before_load)
    cashRepo.save_from_df(ii_csv.get_interest(), portfolio, clear_before_load=False)



