from trader.view import api

from trader.models import Trades, Position, Strategy, Logs

from icecream import ic

from django.utils import timezone


def attempt(strats):
    # достаем список бирж
    list_exchange = set(strats.values_list('exchange', flat=True))
    currentPrice = {}

    # загружаю цены
    for exchange in list_exchange:
        if True:
            currentPrice[exchange] = api.getMarketPrice(exchange)
        else:
            Logs(text=f'ошибка в загрузке цен {exchange}').save()

    for strat in strats:

        # без котировки , переключаемся на след стратегию
        if strat.exchange not in currentPrice:
            continue

        # проверка баланса
        if Position.objects.filter(strat=strat.name, active=True).count() * strat.amount < 0:
            Logs(text=f'не хватает денег на {strat.name}').save()
            continue

        # проверка продажи
        try:
            positions_list = Position.objects.filter(strat=strat.name, active=True)
            pos = positions_list.order_by('strike').first()

            if currentPrice[strat.exchange] > pos.strike:
                try_sell(currentPrice, strat, pos)
        except:
            Losg(text=f'ошибка в продаже{strat.name}')

        # проверка покупки
        try:

            positions_list = Position.objects.filter(strat=strat.name, active=True, ).values_list('buy_price',
                                                                                                  flat=True)
            min = positions_list.order_by('buy_price').first()
            max = positions_list.order_by('buy_price').last()

            if not min:
                min = currentPrice[strat.exchange] + strat.step + 1

            if currentPrice[strat.exchange] and currentPrice[strat.exchange] < min - strat.step or currentPrice[
                strat.exchange] > max + strat.step:
                try_buy(currentPrice, strat)
        except:
            Losg(text=f'ошибка в покупке{strat.name}')


def try_buy(currentPrice, strat):
    # покупка
    amount_usd = round(strat.amount)
    amount_eth = round(strat.amount / currentPrice[strat.exchange], 6)

    trade = Trades.objects.create(strat=strat.name,
                                  types='BUY',
                                  price=currentPrice[strat.exchange],
                                  amount_usd=-amount_usd,
                                  amount_eth=amount_eth
                                  )
    Logs(
        text=f'создал трейд {trade.id, strat.name} - "BUY"- {trade.price, -amount_usd, amount_eth,}').save()

    # открытие позиции
    position = Position.objects.create(strat=strat.name,
                                       buy_price=currentPrice[strat.exchange],
                                       strike=round(currentPrice[strat.exchange] + currentPrice[strat.exchange] * (
                                               strat.profit_percent / 100), 2),
                                       amount_eth=amount_eth
                                       )
    Logs(text=f'''создал позицию {position.id, position.strat, position.buy_price, position.strike, amount_eth}''').save()


def try_sell(currentPrice, strat, pos):
    # продажа
    amount_usd = round(pos.amount_eth * currentPrice[strat.exchange], 2)
    amount_eth = pos.amount_eth


    trade=Trades.objects.create(strat=strat.name,
                          types='SELL',
                          price=currentPrice[strat.exchange],
                          amount_usd=amount_usd,
                          amount_eth=-amount_eth,
                          )
    Logs(
        text=f'''создал трейд {trade.id,trade.strat} - "SELL"- {trade.price,amount_usd,-amount_eth}''').save()

    # закрытие позиции
    try:
        pos.strat = strat.name
        pos.sell_price = currentPrice[strat.exchange]
        pos.closed = timezone.now()
        pos.active = False
        pos.profit = round(
            (pos.sell_price - pos.buy_price) * amount_eth - (pos.sell_price + pos.buy_price) * amount_eth * 0.001, 2)
        pos.save()

        Logs(text=f'закрыл позицию {pos.id, strat.name, pos.sell_price,pos.profit}').save()
    except:
        Logs(text=f' ошибка при закрытии позиции {pos.id, strat.name, pos.sell_price,pos.profit}').save()
