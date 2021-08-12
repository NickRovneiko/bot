from trader.view import api

from trader.models import Trades, Position, Strategy, Logs

from icecream import ic

from django.utils import timezone


def attempt(strats):
    # достаем список бирж
    list_exchange = set(strats.values_list('exchange', flat=True))
    currentPrice = {}

    for exchange in list_exchange:
        try:
            currentPrice[exchange] = api.getMarketPrice(exchange)
        except:
            Logs(text=f'ошибка в загрузке цен {exchange}').save()


    Logs(text=f'тикеры {currentPrice}').save()

    for strat in strats:

        if strat.balance_usd - strat.step <0 :
            positions_list = Position.objects.filter(strat=strat.name, active=True)
            pos = positions_list.order_by('sell_price').last()

            try_sell(currentPrice, strat, pos)

        try:
            positions_list = Position.objects.filter(strat=strat.name, active=True)
            pos = positions_list.order_by('sell_price').first()

            if currentPrice[strat.exchange] > pos.sell_price:
                try_sell(currentPrice, strat, pos)


        except:
            pass

        try:

            positions_list = Position.objects.filter(strat=strat.name, active=True, ).values_list('buy_price',
                                                                                                  flat=True)
            min = positions_list.order_by('buy_price').first()
            max = positions_list.order_by('buy_price').last()

            if not min:
                min = currentPrice[strat.exchange] + strat.step + 1

            if currentPrice[strat.exchange] < min - strat.step or currentPrice[strat.exchange] > max + strat.step:
                try_buy(currentPrice, strat)
        except:
            pass


def try_buy(currentPrice, strat):

        # покупка
        amount_usd = round(strat.amount)
        amount_eth = round(strat.amount / currentPrice[strat.exchange], 6)

        Logs(
            text=f'создаю трейд {strat.name} - "BUY"- {currentPrice[strat.exchange], -amount_usd, amount_eth, strat.balance_usd - amount_usd, strat.balance_eth + amount_eth}').save()
        Trades.objects.create(strat=strat.name,
                              types='BUY',
                              price=currentPrice[strat.exchange],
                              amount_usd=-amount_usd,
                              amount_eth=amount_eth,
                              balance_usd=strat.balance_usd - amount_usd,
                              balance_eth=strat.balance_eth + amount_eth
                              )

        # открытие позиции
        Logs(text=f'''создаю позицию {strat.name,currentPrice[strat.exchange],
                                      round(currentPrice[strat.exchange] + currentPrice[strat.exchange] * (strat.profit_percent / 100), 2),
                                      amount_eth }''').save()
        Position.objects.create(strat=strat.name,
                                buy_price=currentPrice[strat.exchange],
                                sell_price=round(currentPrice[strat.exchange] + currentPrice[strat.exchange] * (
                                        strat.profit_percent / 100), 2),
                                amount_eth=amount_eth
                                )

        # обновление балансов
        Logs(text=f'''меняю балансы {strat.balance_usd - amount_usd,strat.balance_eth + amount_eth }''').save()
        Strategy.objects.filter(name=strat.name).update(
            balance_usd=strat.balance_usd - amount_usd,
            balance_eth=strat.balance_eth + amount_eth
        )


def try_sell(currentPrice, strat, pos):
    # продажа
    amount_usd = round(pos.amount_eth * currentPrice[strat.exchange], 2)
    amount_eth = pos.amount_eth


    Logs(
        text=f'''создаю трейд {strat.name} - "SELL"- {currentPrice[strat.exchange],
                                                     amount_usd,
                                                     -amount_eth,
                                                     strat.balance_usd + amount_usd,
                                                     strat.balance_eth - amount_eth}''').save()
    Trades.objects.create(strat=strat.name,
                          types='SELL',
                          price=currentPrice[strat.exchange],
                          amount_usd=amount_usd,
                          amount_eth=-amount_eth,
                          balance_usd=strat.balance_usd + amount_usd,
                          balance_eth=strat.balance_eth - amount_eth
                          )

    # закрытие позиции
    Logs(text=f'''выбрал {strat.name} закрыть позицию {pos.strat}, sell_price= {currentPrice[strat.exchange]}, страйк= {pos.sell_price}''').save()

    Logs(text=f'''закрываю позицию {strat.name, currentPrice[strat.exchange],
                                  (pos.sell_price - pos.buy_price) * amount_eth - (pos.sell_price + pos.buy_price) * amount_eth * 0.001, 2}''').save()
    pos.strat = strat.name
    pos.sell_price = currentPrice[strat.exchange]
    pos.closed = timezone.now()
    pos.active = False
    pos.profit = round(
        (pos.sell_price - pos.buy_price) * amount_eth - (pos.sell_price + pos.buy_price) * amount_eth * 0.001, 2)
    pos.save()

    # обновление балансов
    Logs(text=f'''меняю балансы {strat.balance_usd + amount_usd, strat.balance_eth - amount_eth}''').save()
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
