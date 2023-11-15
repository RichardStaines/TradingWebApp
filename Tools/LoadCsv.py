import sys
import os
import argparse

from DividendSchedule.models import DivScheduleRepository
from cash.models import *
from dividends.models import *
from trade.models import *
from Utils.iiCSV import IICsv
from portfolio.models import *
from instrument.models import  *
import pandas as pd


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


def load_dividend_schedules_from_csv(filename, clear_before_load):
    df = pd.read_csv(filename, keep_default_na=True)
    df['ex_div_date'] = pd.to_datetime(df['ex_div_date'], format='%d/%m/%Y', errors='coerce')
    df['payment_date'] = pd.to_datetime(df['payment_date'], format='%d/%m/%Y', errors='coerce')
#    print(df.columns)

    db = DivScheduleRepository(debug=True)
    db.save_from_df(df, clear_before_load)
    return df
