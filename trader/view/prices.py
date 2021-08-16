import ccxt
import pandas as pd
import numpy as np
import time

from icecream import ic

from datetime import datetime


def get_prices():
    return


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
    from_timestamp = start
    end = end

    # set timeframe in msecs
    tf_multi = 60 * 1000
    hold = 30

    # make list to hold data
    data = []

    candle_no = (int(end) - int(from_timestamp)) / tf_multi + 1
    ic(f'download {from_timestamp}-{end}')
    while from_timestamp < end:
        try:
            ohlcvs = exchange.fetch_ohlcv(symbol, tf, from_timestamp)

            # если,биржа не отдала данные,  то прибаляю 5 дней
            if not ohlcvs:
                from_timestamp += 4320000000
                continue
            # если биржа отдала замного данных, и переписывает
            elif ohlcvs[-1][0] > end:
                extra_quotes = int((from_timestamp - end) / tf_multi)
                data += ohlcvs[:-extra_quotes]
                from_timestamp = ohlcvs[-1][0]

            else:
                from_timestamp = ohlcvs[-1][0]  # если загрузлось не с co старта,  а с другой даты биржи
                data += ohlcvs


        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
            time.sleep(hold)
    # количество лишних элементов
    extra = int((from_timestamp - end) / tf_multi) + 1
    data = data[:-extra]

    header = ['t', 'o', 'h', 'l', 'c', 'v']
    df = pd.DataFrame(data, columns=header)

    return df


def django_server():
    import os
    import django

    import sys
    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()


if __name__ == '__main__':
    django_server()
