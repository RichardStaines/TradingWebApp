import math

import pandas as pd

# TO Do load from cfg file
sedol_map = {'B6T5S47': 'POLYMETAL',
             'BH0P3Z9': 'BHP',
             '216238': 'AV.',
             'B68SFJ1': 'Hend High Inc',
             'BDR8FC4': 'IND REIT'
             }


class IICsv():

    def __init__(self, filename, debug=False):
        self.filename = filename
        self.debug = debug
        self.load_csv()

    def load_csv(self):
        df = pd.read_csv(self.filename, keep_default_na=True)
        if self.debug:
            print(df.columns)

        df['Description'] = df.apply(lambda row: 'Div' if 'Cash Distrib' in row.Description else row.Description,
                                     axis=1)
        df['Type'] = df.apply(
            lambda row: 'Interest' if row.Description.startswith('GROSS INTEREST')
            else 'Cash' if row.Description == 'SUBSCRIPTION' or row.Description == 'Carried forward cash balance' or row.Description.startswith('PAYMENT')
            else 'Div' if row.Description.startswith('Div') else 'Trade',
            axis=1)

        # if ticker is missing replace with Sedol
        df['Symbol'] = df.apply(
            lambda row: sedol_map[row.Sedol] if str(row.Sedol) in sedol_map else row.Symbol, axis=1)

        df['Symbol'] = df.apply(
            lambda row: "SEDOL:" + str(row.Sedol) if str(row.Symbol) == 'nan' else row.Symbol, axis=1)

        df['Credit'] = df['Credit'].replace('[£,n/a]', '', regex=True).astype(float)
        df['Debit'] = df['Debit'].replace('[£,n/a]', '', regex=True).astype(float)
        df['Amount'] = df.apply(lambda row: row.Credit if math.isnan(row.Credit) is False else -row.Debit, axis=1)
        df['Price'] = df['Price'].replace('[£,n/a]', '', regex=True).astype(float)

        # make the Qty negative for Sells
        df['BuySell'] = df.apply(
            lambda row: 'S' if row.Credit > 0 else r'B', axis=1)

        df['Consideration'] = df.apply(
            lambda row: row.Credit if row.Credit > 0 else row.Debit, axis=1)

        df['Datetime'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
        df['SettleDate'] = pd.to_datetime(df['Settlement Date'], format='%d/%m/%Y', errors='coerce')
        if self.debug:
            print(df.info)

        self.divs = df.loc[df['Description'].str.startswith('Div')]
        if self.debug:
            print(f"Divs\n {self.divs.info}")

        self.interest = df.query('Type == "Interest"')
        if self.debug:
            print(f"Interest\n {self.interest.info}")

        self.trades = df.query('Type == "Trade"')
        if self.debug:
            print(f"\nTrades\n {self.trades.info}")

        self.instruments = self.trades.drop_duplicates(subset=['Symbol']).drop(
            ['Date', 'Settlement Date', 'Quantity', 'Price', 'Reference',
             'Debit', 'Credit', 'Running Balance',
             'BuySell', 'Type', 'Consideration', 'Datetime', 'SettleDate'],
            axis=1)
        if self.debug:
            print(f"\nUnique Instruments\n {self.instruments}")

        self.cash = df.query('Type == "Cash"')
        if self.debug:
            print(f"\nCash\n {self.cash.info}")

    def get_interest(self):
        return self.interest

    def get_cash(self):
        return self.cash

    def get_dividends(self):
        return self.divs

    def get_trades(self):
        return self.trades

    def get_instruments(self):
        return self.instruments

    @staticmethod
    def sum_by_year(df, title=None):
        totals = df.groupby(df['Datetime'].dt.year).agg(Buy_Debit=('Debit' , 'sum'), Sell_Credit=('Credit', 'sum') )
        if title is not None:
            print (f"\n\n{title}:")
        print(totals)

    @staticmethod
    def sum_by_symbol_and_year(df, title=None, include_qty=False):
        if include_qty:
            totals = df.groupby(['Symbol', df['Datetime'].dt.year] ).agg(Qty=('Quantity', 'sum'), Buy_debit=('Debit', 'sum'), Sell_credit=('Credit', 'sum'))
        else:
            totals = df.groupby(['Symbol', df['Datetime'].dt.year] ).agg(Buy_debit=('Debit', 'sum'), Sell_credit=('Credit', 'sum'))
        if title is not None:
            print (f"\n\n{title}:")
        print(totals)

    @staticmethod
    def sum_by_symbol(df, title=None, include_qty=False):
        if include_qty:
            totals = df.groupby('Symbol').agg(Qty=('Quantity', 'sum'), Buy_Debit=('Debit', 'sum'), Sell_Credit=('Credit', 'sum'))
        else:
            # totals = df.groupby('Symbol').agg({'Debit' : 'sum', 'Credit': 'sum'})
            totals = df.groupby('Symbol').agg(Buy_Debit=('Debit', 'sum'), Sell_Credit=('Credit', 'sum'))

        if title is not None:
            print (f"\n\n{title}:")
        print(totals)
