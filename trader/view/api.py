import ccxt
from icecream import ic

exchange = ccxt.kucoin()

markets = exchange.load_markets()


def getMarketPrice():
    price=exchange.fetch_ticker('ETH/USDT')['bid']
    return price








getMarketPrice()


