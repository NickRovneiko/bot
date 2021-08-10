from trader.view import api

from trader.models import Trades, Position, Variables

from icecream import ic

from django.utils import timezone


def attempt(vars):
    currentPrice = api.getMarketPrice()
    try:
        try_sell(currentPrice, vars)

    except:
        pass

    try_buy(currentPrice, vars)



def try_buy(currentPrice, vars):
    postions_list = Position.objects.filter(active=True).values_list('buy_price', flat=True)
    min = postions_list.order_by('buy_price').first()
    max = postions_list.order_by('buy_price').last()

    if not min:
        min=currentPrice+vars.step + 1

    if currentPrice < min - vars.step or currentPrice > max + vars.step:
        # покупка
        amount_usd = round(vars.amount)
        amount_eth = round(vars.amount / currentPrice, 6)

        Trades.objects.create(types='BUY',
                              price=currentPrice,
                              amount_usd=-amount_usd,
                              amount_eth=amount_eth,
                              balance_usd=vars.balance_usd - amount_usd,
                              balance_eth=vars.balance_eth + amount_eth
                              )

        # открытие позиции
        Position.objects.create(buy_price=currentPrice,
                                sell_price=currentPrice + currentPrice * (vars.profit_percent / 100),
                                amount_eth=amount_eth
                                )

        # обновление балансов
        Variables.objects.update(
            balance_usd=vars.balance_usd - amount_usd,
            balance_eth=vars.balance_eth + amount_eth
        )


def try_sell(currentPrice, vars):
    postions_list = Position.objects.filter(active=True)
    pos = postions_list.order_by('sell_price').first()

    if currentPrice > pos.sell_price:
        # продажа
        ic('продажа')
        amount_usd = round(pos.amount_eth * currentPrice, 2)
        amount_eth = pos.amount_eth

        Trades.objects.create(types='SELL',
                              price=currentPrice,
                              amount_usd=amount_usd,
                              amount_eth=amount_eth,
                              balance_usd=vars.balance_usd + amount_usd,
                              balance_eth=vars.balance_eth - amount_eth
                              )

        # закрытие позиции

        pos.sell_price = currentPrice
        pos.closed = timezone.now()
        pos.active = False
        pos.profit = round((pos.sell_price - pos.buy_price) * amount_eth,2)
        pos.save()

        # обновление балансов

        Variables.objects.update(
            balance_usd=vars.balance_usd + amount_usd,
            balance_eth=vars.balance_eth - amount_eth
        )

#     return min,max
#
#
# def get_high_buy:
#
# def tryToBuy(percentageDiff,currentPrice):
#     if percentageDiff >= UPWARD_TREND_THRESHOLD or percentageDiff <= DIP_THRESHOLD:
#         global lastOpPrice, isNextOperationBuy
#         lastOpPrice = placeBuyOrder(currentPrice)
#         isNextOperationBuy = False
#
#
#
# def tryToSell(percentageDiff,currentPrice):
#     if percentageDiff >= PROFIT_THRESHOLD or percentageDiff <= STOP_LOSS_THRESHOLD:
#
#         if percentageDiff <= STOP_LOSS_THRESHOLD:
#             print('фиксирую убытки')
#
#         global lastOpPrice, isNextOperationBuy
#         lastOpPrice = placeSellOrder(currentPrice)
#         isNextOperationBuy = True
#
#
#
#
# def placeBuyOrder(currentPrice):
#     price = api.getMarketPrice()
#     print(f'купил по {price} дельта задержки {round(price/currentPrice *100,2)} ')
#
#     return price
#
# def placeSellOrder(currentPrice):
#     price= api.getMarketPrice()
#     print(f'продал по {price} дельта задержки {round(price/currentPrice *100,2)}')
#
#     return price
#
