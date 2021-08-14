import pandas as pd
import ccxt
import datetime

from icecream import ic

def getMarketPrice(exchange,pair):

    exchange = getattr(ccxt,exchange)()

    markets = exchange.load_markets()

    price = exchange.fetch_ticker(pair)['bid']
    return price


def gather_data():
    exchange = getattr(ccxt, 'binance')()
    markets = exchange.load_markets()
    data = exchange.fetch_ohlcv('ETH/USDT', timeframe='1m')
    df = pd.DataFrame(data)
    # df.columns = (['Date Time', 'Open', 'High', 'Low', 'Close', 'Volume'])

    def parse_dates(ts):
        return datetime.datetime.fromtimestamp(ts / 1000.0)

    # df['DateTime'] = df['DateTime'].apply(parse_dates)

    ic(df)



if __name__ == '__main__':
    gather_data()
