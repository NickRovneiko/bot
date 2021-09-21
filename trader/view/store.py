from icecream import ic

from datetime import datetime

import pandas as pd

from django_pandas.io import read_frame

from trader.models import History, Position, Logs, Tests

from . import prices


def get_historical_price(start=1625097600000, end=1629072000000, exchange='binance',
                         pair='ETH/USDT', type='all', timeframe='1m'):
    if end == 'now':
        end=int(datetime.now().timestamp() * 1000)

    charts = History.objects.filter(exchange=exchange, pair=pair, timeframe=timeframe)

    if not charts.exists():
        df = prices.download_ohlcv(start=start, end=end, exchange=exchange, pair=pair, timeframe=timeframe)
        history_save(df, exchange, pair, timeframe)
        first = True
    else:
        first = False

    # дозагружаю период до имеющегося в базе
    if not first and start < charts.first().timestamp:
        try:
            df = prices.download_ohlcv(start=start, end=charts.first().timestamp - 60000, exchange=exchange, pair=pair,
                                       timeframe=timeframe)
            history_save(df, exchange, pair, timeframe)


        except:
            Logs(text='ошибка загрузки вначале timestamp').save()

    #  дозагружаю период после имеющегося в базе
    if not first and charts.last().timestamp < end:
        try:
            df = prices.download_ohlcv(start=charts.last().timestamp + 1, end=end, exchange=exchange,
                                       pair=pair, timeframe=timeframe)
            history_save(df, exchange, pair, timeframe)

        except:
            Logs(text='ошибка загрузки после timestamp').save()

    qs = History.objects.filter(exchange=exchange,
                                pair=pair,
                                timestamp__gte=start,
                                timeframe=timeframe,
                                ).exclude(timestamp__gte=end)
    df_prices = read_frame(qs)

    if type == 'c':
        df_prices = df_prices[['timestamp', 'close']]

    return df_prices


def history_save(df, exchange='kucoin', pair='ETH/USDT', timeframe='1m'):
    model_instances = [History(exchange=exchange,
                               pair=pair,
                               timeframe=timeframe,
                               timestamp=row['t'],
                               open=row['o'],
                               high=row['h'],
                               low=row['l'],
                               close=row['c'],
                               volume=row['v']) for idx, row in df.iterrows()]
    History.objects.bulk_create(model_instances)


def positions_save(df):
    df = df.where(pd.notnull(df), 0)
    model_instances = [Position(varian=row.varian,
                                buy_price=row.buy_price,
                                sell_price=row.sell_price,
                                strike=row.strike,
                                amount_base=row.amount_base,
                                opened=row.opened,
                                closed=row.closed,
                                active=row.active,
                                profit=row.profit
                                )
                       for idx, row in df.iterrows()]
    Position.objects.bulk_create(model_instances)


def get_df_postions(varian_name='kucoin_1_25_0.4', active=True):
    if Position.objects.filter(varian=varian_name, active=active).exists():
        positions = Position.objects.filter(varian=varian_name)
        df_positions = read_frame(positions)
    else:
        # создаю пустой df
        df_positions = pd.DataFrame(columns=[column.name for column in Position._meta.get_fields()])

    return df_positions


def test_save(varian=False, win_rate=False, profit=False, text=False):
    Tests(
        name=varian.name,
        pair=varian.pair,
        type=varian.type,
        exchange=varian.exchange,
        start_balance=varian.start_balance,
        win_rate=win_rate,
        profit=profit,
        text=text).save()

    return
