from django.core.management.base import BaseCommand
from pytickersymbols import PyTickerSymbols
from pgfinance.models import Company, Price
from pgfinance.chart import Chart
from pandas import DataFrame
import pandas as pd
from django.db.models import Q
from django_pandas.io import read_frame
import mplfinance as mpf
       
def add_indicator(df, type, period):
    if type == "MA":
        df[f"MA{period}"] = df.rolling(window=period)['close'].mean()
    elif type == "BOLL":
        # df["BOLL_low"] = df.rolling(window=period)['close'].mean()
        # df["BOLL_middle"] = df.rolling(window=10)['close'].mean()*1.1
        # df["BOLL_high"] = df.rolling(window=100)['close'].mean()*1.2


        # Calculate the 20-period Standard Deviation (SD)
        df['SD'] = df['close'].rolling(window=20).std()
        # Calculate the 20-period Simple Moving Average (SMA)
        df['BOLL_middle'] = df['close'].rolling(window=20).mean()
        # Calculate the Upper Bollinger Band (UB) and Lower Bollinger Band (LB)
        df['BOLL_high'] = df['BOLL_middle'] + 2 * df['SD']
        df['BOLL_low'] = df['BOLL_middle'] - 2 * df['SD']
    else:
        print(f"Invalid Indicator Type: {period}")
        exit(99)

    print(df.describe)

