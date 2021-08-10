from trader.view import api

from trader.models import Trades, Position, Strategy

from icecream import ic

from django.utils import timezone


def attempt(strats):
    # достаем список бирж
    list_exchange = set(strats.values_list('exchange', flat=True))
    currentPrice = {}

    for exchange in list_exchange:
        currentPrice[exchange] = api.getMarketPrice(exchange)


    for strat in strats:
        try:
            try_sell(currentPrice, strat)

        except:
            pass

        try_buy(currentPrice, strat)


def try_buy(currentPrice, strat):
    positions_list = Position.objects.filter(strat=strat.name, active=True, ).values_list('buy_price', flat=True)
    min = positions_list.order_by('buy_price').first()
    max = positions_list.order_by('buy_price').last()

    if not min:
        min = currentPrice[strat.exchange] + strat.step + 1

    if currentPrice[strat.exchange] < min - strat.step or currentPrice[strat.exchange] > max + strat.step:
        # покупка
        amount_usd = round(strat.amount)
        amount_eth = round(strat.amount / currentPrice[strat.exchange], 6)

        Trades.objects.create(strat=strat.name,
                              types='BUY',
                              price=currentPrice[strat.exchange],
                              amount_usd=-amount_usd,
                              amount_eth=amount_eth,
                              balance_usd=strat.balance_usd - amount_usd,
                              balance_eth=strat.balance_eth + amount_eth
                              )

        # открытие позиции
        Position.objects.create(strat=strat.name,
                                buy_price=currentPrice[strat.exchange],
                                sell_price=round(currentPrice[strat.exchange] + currentPrice[strat.exchange] * (
                                            strat.profit_percent / 100), 2),
                                amount_eth=amount_eth
                                )

        # обновление балансов
        Strategy.objects.filter(name=strat.name).update(
            balance_usd=strat.balance_usd - amount_usd,
            balance_eth=strat.balance_eth + amount_eth
        )


def try_sell(currentPrice, strat):
    positions_list = Position.objects.filter(active=True)
    pos = positions_list.order_by('sell_price').first()

    if currentPrice[strat.exchange] > pos.sell_price:
        # продажа
        amount_usd = round(pos.amount_eth * currentPrice[strat.exchange], 2)
        amount_eth = pos.amount_eth

        Trades.objects.create(strat=strat.name,
                              types='SELL',
                              price=currentPrice[strat.exchange],
                              amount_usd=amount_usd,
                              amount_eth=amount_eth,
                              balance_usd=strat.balance_usd + amount_usd,
                              balance_eth=strat.balance_eth - amount_eth
                              )

        # закрытие позиции
        pos.strat = strat.name
        pos.sell_price = currentPrice[strat.exchange]
        pos.closed = timezone.now()
        pos.active = False
        pos.profit = round((pos.sell_price - pos.buy_price) * amount_eth-(pos.sell_price + pos.buy_price) * amount_eth*0.1, 2)
        pos.save()

        # обновление балансов

        Strategy.objects.filter(name=strat.name).update(
            balance_usd=strat.balance_usd + amount_usd,
            balance_eth=strat.balance_eth - amount_eth
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
