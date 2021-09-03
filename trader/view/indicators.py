def run():
    import os, django, sys

    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()


import pandas as pd

pd.options.display.max_columns = None

from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands, DonchianChannel

from icecream import ic

import json

from trader.view import g


def update_df_by_indicators(df=False):
    if g.strat.indicators:
        try:
            for indicator, params in json.loads(g.strat.indicators).items():
                if isinstance(params, dict):
                    for key, value in params.items():
                        df = eval(indicator)(df=df, key=key, value=value)
        except:
            list_indicator = g.strat.indicators.split(',')
            for indicator in list_indicator:
                df = eval(indicator)(df=df)
    return df


def ma(df, key, value):
    df[key] = df.close.rolling(window=value).mean()

    return df


def bollinger(df):
    indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)

    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    return df


def dochian(df):
    indicator_doc = DonchianChannel(close=df["close"], high=df['high'], low=df['low'], window=10)
    df['doc_h'] = indicator_doc.donchian_channel_hband()
    df['doc_l'] = indicator_doc.donchian_channel_lband()

    return df


def PPVI_bands(df=pd.DataFrame):
    if df.empty:
        df = store.get_historical_price(timeframe='1h')

    df = PPVI(df=df)

    df['ma'] = df.close.rolling(3).mean()
    df['upper_band'] = df.ma + df.max_std_high * 2
    df['bottom_band'] = df.ma - df.max_std_low * 2

    return df


def PPVI(df=pd.DataFrame()):
    if df.empty:
        df = store.get_historical_price(timeframe='1h')

    df['std_high'] = df.high.rolling(3).std()
    df['std_low'] = df.low.rolling(3).std()

    df['max_std_high'] = df.std_high.rolling(3).max()
    df['max_std_low'] = df.std_low.rolling(3).max()

    return df


#
# run()
#
from trader.view import store
# PPVI_bands()
