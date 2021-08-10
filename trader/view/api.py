import ccxt
from icecream import ic

def getMarketPrice(exchange):

    exchange = getattr(ccxt,exchange)()

    markets = exchange.load_markets()

    price=exchange.fetch_ticker('ETH/USDT')['bid']

    return price



