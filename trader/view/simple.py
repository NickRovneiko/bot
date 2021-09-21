

from trader.view import api

isNextOperationBuy = True

PROFIT_THRESHOLD = 0.05
UPWARD_TREND_THRESHOLD = 0.1

STOP_LOSS_THRESHOLD = -0.5
DIP_THRESHOLD = -0.6

lastOpPrice = 100.00


balance=10000







def attemptToMakeTrade():
    currentPrice = api.get_bid_price()
    percentageDiff = (currentPrice - lastOpPrice)/lastOpPrice*100
    if isNextOperationBuy:
        tryToBuy(percentageDiff, currentPrice)
    else:
        tryToSell(percentageDiff,currentPrice)

def tryToBuy(percentageDiff,currentPrice):
    if percentageDiff >= UPWARD_TREND_THRESHOLD or percentageDiff <= DIP_THRESHOLD:
        global lastOpPrice, isNextOperationBuy
        lastOpPrice = placeBuyOrder(currentPrice)
        isNextOperationBuy = False



def tryToSell(percentageDiff,currentPrice):
    if percentageDiff >= PROFIT_THRESHOLD or percentageDiff <= STOP_LOSS_THRESHOLD:

        if percentageDiff <= STOP_LOSS_THRESHOLD:
            print('фиксирую убытки')

        global lastOpPrice, isNextOperationBuy
        lastOpPrice = placeSellOrder(currentPrice)
        isNextOperationBuy = True




def placeBuyOrder(currentPrice):
    price = api.get_bid_price()
    print(f'купил по {price} дельта задержки {round(price/currentPrice *100,2)} ')

    return price

def placeSellOrder(currentPrice):
    price= api.get_bid_price()
    print(f'продал по {price} дельта задержки {round(price/currentPrice *100,2)}')

    return price











