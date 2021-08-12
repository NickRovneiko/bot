from trader.view import api

from trader.models import Trades, Position, Strategy, Logs

from icecream import ic

from django.utils import timezone


def attempt(strats):
    # достаем список бирж
    list_markets = set(strats.values_list('exchange', 'pair'))
    currentPrices = {}

    # загружаю цены
    for market in list_markets:
        if market[0] not in currentPrices:
            currentPrices[market[0]]={}

        try:

            currentPrices[market[0]].update(api.getMarketPrice(market[0], market[1]))
        except:
            Logs(text=f'ошибка в загрузке цен {market}').save()

    ic(currentPrices['huobi'])

    for strat in strats:

        # без котировки , переключаемся на след стратегию
        if strat.exchange in currentPrices:
            if strat.pair in currentPrices[strat.exchange]:
                price = currentPrices[strat.exchange][strat.pair]
            else:
                continue
        else:
            continue



        # проверка баланса
        if strat.balance_usd - Position.objects.filter(strat=strat.name, active=True).count() * strat.amount-strat.amount < 0:
            continue

        # проверка продажи
        try:
            positions_list = Position.objects.filter(strat=strat.name, active=True).order_by('strike')

            for pos in positions_list:
                if price > pos.strike:
                    try_sell(price, strat, pos)
                else:
                    break
        except:
            Logs(text=f'ошибка в продаже {strat.name}').save()

        # проверка покупки
        try:

            positions_list = Position.objects.filter(strat=strat.name, active=True, ).values_list('buy_price',
                                                                                                  flat=True)
            min = positions_list.order_by('buy_price').first()
            max = positions_list.order_by('buy_price').last()

            if not min:
                min = price + strat.step + 1

            if price < min - strat.step or price > max + strat.step:
                try_buy(price, strat)
        except:
            Logs(text=f'ошибка в покупке{strat.name}').save()


def try_buy(price, strat):
    # покупка
    amount_usd = round(strat.amount)
    amount_eth = round(strat.amount / price, 6)

    trade = Trades.objects.create(strat=strat.name,
                                  types='BUY',
                                  price=price,
                                  amount_usd=-amount_usd,
                                  amount_eth=amount_eth
                                  )
    Logs(
        text=f'создал трейд {trade.id, strat.name} - "BUY"- {trade.price, -amount_usd, amount_eth,}').save()

    # открытие позиции
    position = Position.objects.create(strat=strat.name,
                                       buy_price=price,
                                       strike=round(price + price * (strat.profit_percent / 100), 2),
                                       amount_eth=amount_eth
                                       )
    Logs(
        text=f'''создал позицию {position.id, position.strat, position.buy_price, position.strike, amount_eth}''').save()


def try_sell(price, strat, pos):
    # продажа
    amount_usd = round(pos.amount_eth * price, 2)
    amount_eth = pos.amount_eth

    trade = Trades.objects.create(strat=strat.name,
                                  types='SELL',
                                  price=price,
                                  amount_usd=amount_usd,
                                  amount_eth=-amount_eth,
                                  )
    Logs(
        text=f'''создал трейд {trade.id, trade.strat} - "SELL"- {trade.price, amount_usd, -amount_eth}''').save()

    # закрытие позиции
    try:
        pos.strat = strat.name
        pos.sell_price = price
        pos.closed = timezone.now()
        pos.active = False
        pos.profit = round(
            (pos.sell_price - pos.buy_price) * amount_eth - (pos.sell_price + pos.buy_price) * amount_eth * 0.001, 2)
        pos.save()

        Logs(text=f'закрыл позицию {pos.id, strat.name, pos.sell_price, pos.profit}').save()
    except:
        Logs(text=f' ошибка при закрытии позиции {pos.id, strat.name, pos.sell_price, pos.profit}').save()

