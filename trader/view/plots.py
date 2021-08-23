import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt

from django_pandas.io import read_frame

from trader.models import History, Position

from icecream import ic

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt


def run():
    pd.options.display.max_columns = None

    exchange = 'binance'
    pair = 'ETH/USDT'

    start = 1627776000000
    end = 1629072000000
    varian = 'ETH/USDT 10_10_1'

    qs = History.objects.filter(exchange=exchange,
                                pair=pair,
                                timestamp__gte=start,
                                timeframe='1m'
                                ).exclude(timestamp__gte=end)
    df = read_frame(qs)

    # df = df[['timestamp', 'open', 'close', 'low', 'high']]
    df = df[['timestamp', 'open']]

    # qs = Position.objects.filter(varian=varian,
    #                              opened__gte=start,
    #                              ).exclude(opened__gte=end)
    #
    # df_qs = read_frame(qs)
    #
    # df_buy = df_qs[['opened', 'buy_price']]
    # df_buy = df_buy.rename(columns={'opened': 'timestamp'})
    #
    # df = df.merge(df_buy, left_on='timestamp', right_on='timestamp', how='left')
    #
    # df_sell = df_qs[['closed', 'sell_price']]
    # df_sell = df_sell.rename(columns={'closed': 'timestamp'})
    #
    # df = df.merge(df_sell, left_on='timestamp', right_on='timestamp', how='left')
    #
    # df['timestamp'] = df['timestamp'].values.astype(dtype='datetime64[ms]')

    df['SMA_120'] = df.iloc[:, 1].rolling(window=120).mean()
    df['SMA_360'] = df.iloc[:, 1].rolling(window=360).mean()
    df.index = df.timestamp

    ic(df)

    plt.figure()
    plt.grid(True)
    plt.plot(df['open'], label='Price')
    plt.plot(df['SMA_120'], label='SMA 120')
    plt.plot(df['SMA_360'], label='SMA 360')
    plt.show()

    plt.show()

    # fig = go.Figure()
    #
    # fig.add_trace((go.Ohlc(
    #     x=df['timestamp'],
    #     open=df['open'],
    #     high=df['high'],
    #     low=df['low'],
    #     close=df['close'],
    #     increasing_line_color='cyan', decreasing_line_color='gray'
    # )))
    #
    # fig.add_traces(go.Scatter(x=df['timestamp'], y=df['buy_price'], mode='markers'))
    # fig.add_traces(go.Scatter(name='Sell', x=df['timestamp'], y=df['sell_price'], mode='markers',
    #                           marker_color='rgba(255, 182, 193, .9)'))
    #
    # fig.update_xaxes(rangeslider_visible=True)
    # fig.show()
