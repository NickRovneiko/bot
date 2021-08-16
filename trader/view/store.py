from icecream import ic

from datetime import datetime

import pandas as pd

from django_pandas.io import read_frame

from trader.models import History, Position, Logs

from . import prices


def get_historical_price(start=1625097600000, end=int(datetime.now().timestamp() * 1000), exchange='kucoin',
                         pair='ETH/USDT', type='o'):
    ic(exchange, pair)
    charts = History.objects.filter(exchange=exchange, pair=pair)

    if not charts.exists():
        df = prices.download_ohlcv(start=start, end=end, exchange=exchange, pair=pair)
        history_save(df, exchange, pair)
        first = True
    else:
        first = False

    # дозагружаю период до имеющегося в базе
    if not first and start < charts.first().timestamp:
        try:
            df = prices.download_ohlcv(start=start, end=charts.first().timestamp - 60000, exchange=exchange, pair=pair)
            history_save(df, exchange, pair)


        except:
            Logs(text='ошибка загрузки вначале timestamp').save()

    #  дозагружаю период после имеющегося в базе
    if not first and charts.last().timestamp < end:
        try:
            df = prices.download_ohlcv(start=charts.last().timestamp + 1, end=end, exchange=exchange,
                                       pair=pair)
            history_save(df, exchange, pair)

        except:
            Logs(text='ошибка загрузки после timestamp').save()

    qs = History.objects.filter(exchange=exchange,
                                pair=pair,
                                timestamp__gte=start,
                                ).exclude(timestamp__gte=end)
    df_prices = read_frame(qs)

    if type == 'o':
        df_prices = df_prices[['timestamp', 'open']]

    return df_prices


def history_save(df, exchange='kucoin', pair='ETH/USDT'):
    model_instances = [History(exchange=exchange,
                               pair=pair,
                               timestamp=row['t'],
                               open=row['o'],
                               high=row['h'],
                               low=row['l'],
                               close=row['c'],
                               volume=row['v']) for idx, row in df.iterrows()]
    History.objects.bulk_create(model_instances)


def positions_save(df):
    model_instances = [Position(varian=row.varian,
                                buy_price=row.buy_price,
                                strike=row.strike,
                                amount_eth=row.amount_eth,
                                opened=row.opened,
                                active=row.active
                                )
                       for idx, row in df.iterrows()]
    Position.objects.bulk_create(model_instances)


def get_df_postions(varian_name='kucoin_1_25_0.4'):
    if Position.objects.filter(varian=varian_name).exists():
        positions = Position.objects.filter(varian=varian_name)
        df_positions = read_frame(positions)
    else:
        # создаю пустой df
        columns = [column.name for column in Position._meta.get_fields()]
        df_positions = pd.DataFrame(columns=columns)

    return df_positions
