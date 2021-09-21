import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

from django_pandas.io import read_frame

from trader.models import Position, Strategies

from trader.view import store, indicators, g

from icecream import ic

import json


def get_chart_varian(varian):
    df_positions = read_frame(
        Position.objects.filter(varian=varian.name)
    )

    if len(df_positions) > 500:
        df_positions = df_positions.sample(n=500)

    g.strat = Strategies.objects.get(variants=varian.type)

    exchange = varian.exchange
    pair = varian.pair

    start = df_positions.iloc[-1].opened
    end = 1629072000000

    df = store.get_historical_price(type='all', start=start, end=end, exchange=exchange, pair=pair, timeframe='1m')

    df = df[['timestamp', 'open', 'close', 'low', 'high']]
    # df = df[['timestamp', 'close']]

    # соеденяя график цены и позиции
    # df_buy = df_positions[['opened', 'buy_price']]
    # df_buy = df_buy.rename(columns={'opened': 'timestamp'})
    #
    # df = df.merge(df_buy, left_on='timestamp', right_on='timestamp', how='outer')
    #
    # df_sell = df_positions[['closed', 'sell_price']].sort_values('closed')
    # df_sell = df_sell[df_sell.sell_price > 0]
    # df_sell = df_sell[df_sell.closed > 0]
    # df_sell = df_sell.rename(columns={'closed': 'timestamp'})
    #
    # df = df.merge(df_sell, left_on='timestamp', right_on='timestamp', how='outer')

    # создаю ma
    # for key, value in json.loads(Strategies.objects.get(variants=varian.type).indicators)['ma'].items():
    #     df = indicators.ma(df, key=key, value=round(value / 60))

    # df=indicators.bollinger(df)
    # df=indicators.dochian(df)


    # добавляю индикаторы
    df=indicators.update_df_by_indicators(df)

    df=df.dropna()

    # удаляю открытую позицию
    df_positions = df_positions[df_positions.closed > 0]







    # timestamp перевожу в дату
    df_positions['opened'] = df_positions['opened'].values.astype(dtype='datetime64[ms]')
    df_positions['closed'] = df_positions['closed'].values.astype(dtype='datetime64[ms]')
    df['timestamp'] = df['timestamp'].values.astype(dtype='datetime64[ms]')
    df.index = df.timestamp


    # # вставляю пустую строчку для отрезков
    # i=2
    # new_df=df_positions[:1]
    #
    # for idx, row in df_positions.iterrows():
    #     if i < 2:
    #         new_df=new_df.append(row, ignore_index=True)
    #         i += 1
    #         continue
    #     else:
    #         new_df = new_df.append(pd.Series(), ignore_index=True)
    #         i=1
    # ic(new_df)
    # exit()

    from plotly.offline import plot
    graphs = []

    # Setting layout of the figure.
    layout = {
        'yaxis_title': pair,
        'height': 700,
        'width': 1400,
    }

    # df=indicators

    fig = go.Figure(layout=layout)


    for column in df.columns[1:]:
        fig.add_trace(
            go.Scattergl(x=df['timestamp'], y=df[column], mode='lines',name=column)
        )

    fig.add_trace(
        go.Scattergl(x=df_positions['opened'], y=df_positions['buy_price'], mode='markers', name='buy',
                   line=dict(
                       color='green',
                       width=5)
                   )
    )

    fig.add_trace(
        go.Scattergl(x=df_positions['closed'], y=df_positions['sell_price'], mode='markers', name='sell',
                   line=dict(
                       color='red',
                       width=5)
                   )
    )

    #PPV
    #fig.add_trace(
    #     go.Scatter(x=df['timestamp'], y=df['fast'], mode='lines', name='fast',
    #                line=dict(
    #                    color='yellow')
    #                )
    # )




    # ma_cross
    # fig.add_trace(
    #     go.Scatter(x=df['timestamp'], y=df['fast'], mode='lines', name='fast',
    #                line=dict(
    #                    color='yellow')
    #                )
    # )
    #
    # fig.add_trace(
    #     go.Scatter(x=df['timestamp'], y=df['slow'], mode='lines', name='slow',
    #                line=dict(
    #                    color='brown')
    #                )
    # )

    # маркеры
    fig.add_trace(
        go.Scattergl(x=df_positions.opened,
                   y=df_positions.buy_price - df_positions.buy_price * 0.03,
                   mode='markers',
                   name='buy',
                   marker=go.Marker(size=15,
                                    symbol="triangle-up",
                                    color='green')
                   )
    )

    fig.add_trace(
        go.Scattergl(x=df_positions.closed,
                   y=df_positions.sell_price + df_positions.sell_price * 0.03,
                   mode='markers',
                   name='sell',
                   marker=go.Marker(size=15,
                                    symbol="triangle-down",
                                    color='red')
                   )
    )



    # graphs.append(
    #     go.Scatter(x=df['timestamp'], y=df['doc_h'], mode='lines', name='doc_h',
    #                line=dict(
    #                    color='black')
    #                )
    # )
    #
    # graphs.append(
    #     go.Scatter(x=df['timestamp'], y=df['doc_l'], mode='lines', name='doc_l',
    #                line=dict(
    #                    color='black')
    #                )
    # )
    # df['bb_bbm'] = indicator_bb.bollinger_mavg()


    data= fig.to_html()

    return data
