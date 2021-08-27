import plotly.express as px
import plotly.graph_objects as go

from django_pandas.io import read_frame

from trader.models import Position, Strategies

from trader.view import store, indicators

from icecream import ic

import json


def get_chart_varian(varian):

    df_positions = read_frame(
        Position.objects.filter(varian=varian.name)
    )
    if len(df_positions) > 300:
        df_positions = df_positions.sample(n=300)

    exchange = varian.exchange
    pair = varian.pair

    start = df_positions.iloc[-1].opened
    end = 1629072000000


    df = store.get_historical_price(type='all',start=start, end=end, exchange=exchange, pair=pair, timeframe='1h')

    df = df[['timestamp', 'open', 'close', 'low', 'high']]
    # df = df[['timestamp', 'close']]

    df_buy = df_positions[['opened', 'buy_price']]
    df_buy = df_buy.rename(columns={'opened': 'timestamp'})

    df = df.merge(df_buy, left_on='timestamp', right_on='timestamp', how='outer')

    df_sell = df_positions[['closed', 'sell_price']].sort_values('closed')
    df_sell = df_sell[df_sell.sell_price > 0]
    df_sell = df_sell[df_sell.closed > 0]
    df_sell = df_sell.rename(columns={'closed': 'timestamp'})

    df = df.merge(df_sell, left_on='timestamp', right_on='timestamp', how='outer')


    # создаю ma

    for key, value in json.loads(Strategies.objects.get(variants=varian.type).indicators)['ma'].items():
        df = indicators.ma(df, name=key, period=round(value/60))

    # df=indicators.bollinger(df)
    df=indicators.dochian(df)



    df['timestamp'] = df['timestamp'].values.astype(dtype='datetime64[ms]')
    df.index = df.timestamp


    from plotly.offline import plot
    graphs = []

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['close'], mode='lines', name='Price', )
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
        go.Scatter(x=df['timestamp'], y=df['fast'], mode='lines', name='fast',
                   line=dict(
                       color='yellow')
                   )
    )

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['slow'], mode='lines', name='slow',
                   line=dict(
                       color='brown')
                   )
    )

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['doc_h'], mode='lines', name='doc_h',
                   line=dict(
                       color='black')
                   )
    )

    graphs.append(
        go.Scatter(x=df['timestamp'], y=df['doc_l'], mode='lines', name='doc_l',
                   line=dict(
                       color='black')
                   )
    )
    #df['bb_bbm'] = indicator_bb.bollinger_mavg()


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