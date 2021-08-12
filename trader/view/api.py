import ccxt
from icecream import ic

def getMarketPrice(exchange,pair):

    exchange = getattr(ccxt,exchange)()

    markets = exchange.load_markets()

    price={pair:exchange.fetch_ticker(pair)['bid']}
    return price



