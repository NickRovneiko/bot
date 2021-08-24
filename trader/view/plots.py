import plotly.express as px
import plotly.graph_objects as go

from django_pandas.io import read_frame

from trader.models import History, Position, Variants

from trader.view import store

from icecream import ic

import pandas as pd

import numpy as np
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

def get_chart_varian(varian_id):
    varian = Variants.objects.get(id=varian_id)

    df_positions = read_frame(
        Position.objects.filter(varian=varian.name)
    )
    if len(df_positions) > 300:
        df_positions = df_positions.sample(n=300)

    exchange = varian.exchange
    pair = varian.pair

    start = df_positions.iloc[-1].opened
    end = 1629072000000


    df = store.get_historical_price(start=start, end=end, exchange=exchange, pair=pair, timeframe='1h')

    # df = df[['timestamp', 'open', 'close', 'low', 'high']]
    df = df[['timestamp', 'open']]

    df_buy = df_positions[['opened', 'buy_price']]
    df_buy = df_buy.rename(columns={'opened': 'timestamp'})

    df = df.merge(df_buy, left_on='timestamp', right_on='timestamp', how='outer')

    df_sell = df_positions[['closed', 'sell_price']].sort_values('closed')
    df_sell = df_sell[df_sell.sell_price > 0]
    df_sell = df_sell[df_sell.closed > 0]
    df_sell = df_sell.rename(columns={'closed': 'timestamp'})

    df = df.merge(df_sell, left_on='timestamp', right_on='timestamp', how='outer')
    df['timestamp'] = df['timestamp'].values.astype(dtype='datetime64[ms]')

    df['short'] = df.iloc[:, 1].rolling(window=6).mean()
    df['long'] = df.iloc[:, 1].rolling(window=48).mean()
    df.index = df.timestamp


    from plotly.offline import plot
    graphs = []

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['open'], mode='lines', name='Price', )
    )
    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['buy_price'], mode='markers', name='buy',
                   line=dict(
                       color='green',
                       width=5)
                   )
    )

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['sell_price'], mode='markers', name='sell',
                   line=dict(
                       color='red',
                       width=5)
                   )
    )

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['short'], mode='lines', name='short',
                   line=dict(
                       color='yellow')
                   )
    )

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['long'], mode='lines', name='long',
                   line=dict(
                       color='brown')
                   )
    )

    # Setting layout of the figure.
    layout = {
        'yaxis_title': pair,
        'height': 700,
        'width': 1400,
    }
    # Getting HTML needed to render the plot.
    data = plot({'data': graphs, 'layout': layout},
                output_type='div')

    return data


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

    plt.figure()
    plt.grid(True)
    plt.plot(df['open'], label='Price')
    plt.plot(df['SMA_120'], label='SMA 120')
    plt.plot(df['SMA_360'], label='SMA 360')
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
