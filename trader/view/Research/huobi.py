import ccxt

from icecream import ic





exchange =ccxt.huobi({'options':{'defaultType': 'future'}})
exchange.load_markets()


ic(len(exchange.markets))