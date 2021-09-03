from icecream import  ic


#  MarketData
from kucoin_futures.client import Market, Trade, User
client = Market(url='https://api-futures.kucoin.com')




def symbol_list():
    result=client.get_contracts_list()
    symbol_list=[]
    for row in result:
       symbol_list.append(row['symbol'])

    return symbol_list

def get_order_book(pair='ETHUSDM'):
    order_book = client.l2_order_book(pair)

    return order_book


def get_ticker(pair='ETHUSDM'):
    klines = client.get_ticker(pair)

    return klines

# get symbol ticker
# server_time = client.get_server_timestamp()
#
api_key = '612d1976381a62000688b108'
api_secret = '17df6245-67ce-4901-934f-feb8079c8aba'
api_passphrase = '7hqefwvJ6H3z'
#

# Trade
# client = Trade(key='', secret='', passphrase='', is_sandbox=False, url='')



#
# # or connect to Sandbox
# # client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)
#
# # place a limit buy order
# order_id = client.create_limit_order('XBTUSDM', 'buy', '1', '30', '8600')
#
# # place a market buy order   Use cautiously
# order_id = client.create_market_order('XBTUSDM', 'buy', '1')
#
# # cancel limit order
# client.cancel_order('5bd6e9286d99522a52e458de')
#
# # cancel all limit order
# client.cancel_all_limit_order('XBTUSDM')



def user():
    client = User(api_key, api_secret, api_passphrase)
    result = client.get_accounts()
    ic(result)
#
# # or connect to Sandbox
# # client = User(api_key, api_secret, api_passphrase, is_sandbox=True)
#
# address = client.get_withdrawal_quota('XBT')


# ic(symbol_list())
# get_ticker(pair='UNIUSDTM')
user()