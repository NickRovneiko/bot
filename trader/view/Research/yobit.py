import ccxt
from icecream import ic

def getMarketPrice(pair):

    exchange = getattr(ccxt,'yobit')()

    markets = exchange.load_markets()

    price = exchange.fetch_ticker(pair)
    return price


if __name__=='__main__':

    pair='MOJO/DOGE'

    price=getMarketPrice(pair)

    ic(price)