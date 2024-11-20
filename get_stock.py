#!/usr/bin/env python

import sys
from random import choice
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer

import requests
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import yfinance as yf

def get_latest_stock_price(stock):
    data = stock.history()
    latest_stock_price = data['Close'].iloc[-1]
    return latest_stock_price

def get_today():
    return date.today()

def get_next_day_str(today):
    return get_date_from_string(today) + timedelta(days=1)

def get_date_from_string(expiration_date):
    return datetime.strptime(expiration_date, "%Y-%m-%d").date()

def get_string_from_date(expiration_date):
    return expiration_date.strftime('%Y-%m-%d')

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('ticker', default='QQQ')
    args = parser.parse_args()

    # read the ticker
    ticker = args.ticker
    print('ticker', ticker)

    i = 0
    # Produce data by repeatedly fetching today's stock prices - feel free to change
    while i < 5:

        # date range
        ed = get_today() + timedelta(days=-1)
        sd = ed + timedelta(days=-1)
        dfvp = yf.download(tickers=ticker, start=sd, end=ed, interval="1m")

        topic = ticker
        for index, row in dfvp.iterrows():
            print(index, row['Close']) # debug only
            time.sleep(5)

        print("Fetching again..")
        i += 1
