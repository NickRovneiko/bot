import pandas as pd
import ccxt
import datetime

from icecream import ic

def get_bid_price(exchange:str(), pair:str()):

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

def get_history_deribit(pair='ETH-18SEP21-3600-P'):
    exchange = getattr(ccxt, 'deribit')()
    markets = exchange.load_markets()
    data = exchange.fetch_ohlcv(symbol=pair,
                         limit=1000,
                         since=1631923201000)

    ic(len(data))
    ic(data)

    return


def get_quote(exchange:str(), pair:str()):

    exchange = getattr(ccxt,exchange)()

    markets = exchange.load_markets()

    price = exchange.fetch_ticker(pair)

    return price

def get_markets(exchange:str()):

    exchange = getattr(ccxt,exchange)()

    markets = exchange.load_markets()

    market = exchange.markets


    return market

if __name__ == '__main__':
    pair='ETH-PERPETUAL'#'ETH-20SEP21-3400-P'
    result = get_quote(exchange='deribit', pair=pair)
    ic(result)

