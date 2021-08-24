import plotly.express as px
import plotly.graph_objects as go

from django_pandas.io import read_frame

from trader.models import History, Position, Variants

from trader.view import store

from icecream import ic

import pandas as pd

import numpy as np


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