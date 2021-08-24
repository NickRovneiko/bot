import ccxt
import pandas as pd
import numpy as np
import time

from icecream import ic

from datetime import datetime

from django_pandas.io import read_frame


def get_historical_price(start=1625097600000, end=int(datetime.now().timestamp() * 1000), exchange='kucoin',
                         pair='ETH/USDT'):
    from trader.models import History

    charts = History.objects.filter(exchange=exchange, pair=pair)

    if not charts.exists():
        df = download_ohlcv(start=start, end=end, exchange='kucoin', pair='ETH/USDT')
        save_to_model(df, exchange, pair)
        first = True
    else:
        first=False

    # дозагружаю период до имеющегося в базе
    if not first and start < charts.first().timestamp:
        try:
            df = download_ohlcv(start=start, end=charts.first().timestamp-60000, exchange='kucoin', pair='ETH/USDT')
            save_to_model(df, exchange, pair)


        except:
            ic('ошибка загрузки вначале timestamp')

        #  дозагружаю период после имеющегося в базе
        if not first and charts.last().timestamp < end:
            try:
                df = download_ohlcv(start=charts.first().timestamp+60000, end=end, exchange='kucoin', pair='ETH/USDT')
                save_to_model(df, exchange, pair)

            except:
                ic('ошибка загрузки после timestamp')

    qs = History.objects.filter(exchange=exchange,
                                pair=pair,
                                timestamp__gte=start,
                                ).exclude(timestamp__gte=end)
    df_prices = read_frame(qs)
    ic(df_prices)

    return df_prices


def download_ohlcv(start=1625097600000, end=int(datetime.now().timestamp() * 1000), exchange='kucoin',
                   pair='ETH/USDT'):
    np.set_printoptions(threshold=np.inf)

    exchange = getattr(ccxt, exchange)()

    # exchange = ccxt.exmo({
    #     'apiKey': 'K-...',
    #     'secret': 'S-...',
    # })

    symbol = pair
    tf = '1m'
    from_timestamp = exchange.parse8601('2021-08-01 00:00:00')
    end = exchange.parse8601('2021-08-13 08:00:00')

    # set timeframe in msecs
    tf_multi = 60 * 1000
    hold = 30

    # make list to hold data
    data = []

    candle_no = (int(end) - int(from_timestamp)) / tf_multi + 1
    ic(f'download {exchange}-{pair}')
    while from_timestamp < end:
        try:
            ohlcvs = exchange.fetch_ohlcv(symbol, tf, from_timestamp)
            from_timestamp += len(ohlcvs) * tf_multi
            data += ohlcvs
        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)

    header = ['t', 'o', 'h', 'l', 'c', 'v']
    df = pd.DataFrame(data, columns=header)
    df = df.to_dict('records')

    return df

    # if __name__ == '__main__':
    import os
    import django
    import sys

    # add your project directory to the sys.path
    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    # set environment variable to tell django where your settings.py is
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'

    django.setup()

    def startBot():
        ic()
        from trader.view.strateg import volat

        from trader.models import Variants

        strats = Variants.objects.all()
        volat.backtest_all(strats)

    startBot()
    ic('тест закончен')


def django_server():
    import os
    import django

    import sys
    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()


def save_to_model(df, exchange='kucoin', pair='ETH/USDT'):
    from trader.models import History

    list_records = [History(exchange=exchange,
                            pair=pair,
                            timestamp=row['t'],
                            open=row['o'],
                            high=row['h'],
                            low=row['l'],
                            close=row['c'],
                            volume=row['v']
                            ) for row in df]

    History.objects.bulk_create(list_records)


if __name__ == '__main__':
    django_server()

    get_historical_price()
