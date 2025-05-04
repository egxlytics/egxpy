from tvDatafeed import TvDatafeedLive, TvDatafeed, Interval
from retry import retry
import time
from datetime import timedelta, date
import datetime as dt
import pandas as pd
import numpy as np
import holidays
from datetime import datetime as dt


@retry((Exception), tries=20, delay=0.5, backoff=0)
def get_OHLCV_data(symbol,exchange,interval,n_bars):
    """fetches close prices for a single ticker

    Args:
        symbol (str): Ticker
        exchange (str): Exchange
        interval (str): ['Daily', 'Weekly','Monthly']
        n_bars (int): Last n bars

    Returns:
        pd.DataFrame: response
    """

    interval_dic = {'Daily':Interval.in_daily, 'Weekly':Interval.in_weekly, 'Monthly':Interval.in_monthly}


    tv = TvDatafeedLive()
    response = tv.get_hist(symbol=symbol,
                    exchange=exchange,interval=interval_dic[interval], n_bars=n_bars, timeout=-1)
    return response



@retry((Exception), tries=20, delay=0.5, backoff=0)
def _get_intraday_close_price_data(symbol,exchange,interval,n_bars):
    """fetches close prices for a single ticker

    Args:
        symbol (str): Ticker
        exchange (str): Exchange
        interval (str): ['1 Minute', '5 Minute','30 Minute']
        n_bars (int): Last n bars

    Returns:
        pd.DataFrame: response
    """

    interval_dic = {'1 Minute':Interval.in_1_minute, '5 Minute':Interval.in_5_minute, '30 Minute':Interval.in_30_minute}


    tv = TvDatafeedLive()
    response = tv.get_hist(symbol=symbol,
                    exchange=exchange,interval=interval_dic[interval], n_bars=n_bars, timeout=-1)['close']
    return response

@retry((Exception), tries=20, delay=0.5, backoff=0)
def _get_close_price_data(symbol,exchange,interval,n_bars):
    """fetches close prices for a single ticker

    Args:
        symbol (str): Ticker
        exchange (str): Exchange
        interval (str): ['Daily', 'Weekly','Monthly']
        n_bars (int): Last n bars

    Returns:
        pd.DataFrame: response
    """

    interval_dic = {'Daily':Interval.in_daily, 'Weekly':Interval.in_weekly, 'Monthly':Interval.in_monthly}


    tv = TvDatafeed()
    response = tv.get_hist(symbol=symbol,
                    exchange=exchange,interval=interval_dic[interval], n_bars=n_bars)['close']
    return response



def get_EGXdata(stock_list:list, interval:str, start:date, end:date):
    """Fetches Historical close prices data for EGX stocks


    Args:
        stock_list (list): desired stock list
        interval (str): ['Daily', 'Weekly','Monthly']
        start (date): starting date
        end (date): end date

    Returns:
        _type_: _description_
    """

    n = holidays.country_holidays('EG').get_working_days_count(start,end)



    close_prices_dic = {}
    try:
        for stock in stock_list:
            close = _get_close_price_data(symbol=stock,exchange='EGX',interval=interval,n_bars=n)
            close_prices_dic[stock]=close
    except:
        pass
    df = pd.concat(close_prices_dic,axis=1)
    df.index = pd.to_datetime(df.index.date)
    df.index.name = 'Date'


    return df.loc[start:end,:]


def get_EGX_intraday_data(stock_list:list, interval:str, start:date, end:date):
    """Fetches intraday data for EGX stocks

    Args:
        stock_list (list): desired stocks
        interval (str): ['1 Minute', '5 Minute','30 Minute']
        start (date): starting date
        end (date): end date

    Returns:
        pd.DataFrame: close prices
    """

    n =5000



    close_prices_dic = {}
    try:
        for stock in stock_list:
            close = _get_intraday_close_price_data(symbol=stock,exchange='EGX',interval=interval,n_bars=n)
            close_prices_dic[stock]=close
    except:
        pass
    df = pd.concat(close_prices_dic,axis=1)

    return df.loc[start:end,:].tz_localize("Europe/London").tz_convert("UTC+02:00")
