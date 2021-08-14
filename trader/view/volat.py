from trader.view import api, backtest

from trader.models import Trades, Position, Strategy, Logs

from icecream import ic

from django.utils import timezone


def attempt(strats):
    # достаем список бирж
    list_markets = set(strats.values_list('exchange', 'pair'))
    currentPrices = {}
    # ic()

    # загружаю цены
    for market in list_markets:
        if market[0] not in currentPrices:
            currentPrices[market[0]] = {}

        try:

            currentPrices[market[0]].update({market[1]: api.getMarketPrice(market[0], market[1])})
        except:
            Logs(text=f'ошибка в загрузке цен {market}').save()

    # ic(currentPrices['huobi'])

    for strat in strats:

        # без котировки , переключаемся на след стратегию
        if strat.exchange in currentPrices:
            if strat.pair in currentPrices[strat.exchange]:
                price = currentPrices[strat.exchange][strat.pair]
            else:
                continue
        else:
            continue

        run_strat(strat, price)


def run_strat(strat, price):
    # проверка продажи
    check_sell(strat, price)

    # проверка баланса
    if not check_balance(strat):
        return

    # проверка покупки
    check_buy(strat, price)


def check_sell(strat, price):
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


def check_buy(strat, price):
    # проверка покупки
    try:

        positions_list = Position.objects.filter(strat=strat.name, active=True, ).order_by('buy_price')
        min = positions_list.order_by('buy_price').first()
        max = positions_list.order_by('buy_price').last()

        # если это первый ордер
        if not min:
            try_buy(price, strat)
            return

        # делаем задним числом  вставки на покупку вниз по стакану
        i = 1
        while price < (min.buy_price - strat.step * i):
            try_buy(min.buy_price - strat.step * i, strat)
            i = i + 1
            if not check_balance(strat) or not strat.limit_orders_buy:
                break

        # делаем задним числом  вставки на покупку вверх по стакану

        i = 1
        while price > (max.buy_price + strat.step * i):
            try_buy((max.buy_price + strat.step * i), strat)
            i = i + 1
            if not check_balance(strat) or not strat.limit_orders_buy:
                break

    except:
        Logs(text=f'ошибка в покупке{strat.name}').save()


def try_buy(price, strat):
    # покупка
    amount_usd = round(strat.amount)
    amount_eth = round(strat.amount / price, 6)

    Trades.objects.create(strat=strat.name,
                          types='BUY',
                          price=price,
                          amount_usd=-amount_usd,
                          amount_eth=amount_eth
                          )
    # Logs(
    #     text=f'создал трейд {trade.id, strat.name} - "BUY"- {trade.price, -amount_usd, amount_eth,}').save()

    # открытие позиции
    Position.objects.create(strat=strat.name,
                            buy_price=price,
                            strike=round(price + price * (strat.profit_percent / 100), 2),
                            amount_eth=amount_eth
                            )
    # Logs(
    #     text=f'''создал позицию {position.id, position.strat, position.buy_price, position.strike, amount_eth}''').save()


def try_sell(price, strat, pos):
    # продажа
    amount_usd = round(pos.amount_eth * price, 2)
    amount_eth = pos.amount_eth

    Trades.objects.create(strat=strat.name,
                          types='SELL',
                          price=price,
                          amount_usd=amount_usd,
                          amount_eth=-amount_eth,
                          )
    # Logs(
    #     text=f'''создал трейд {trade.id, trade.strat} - "SELL"- {trade.price, amount_usd, -amount_eth}''').save()

    # закрытие позиции
    try:
        pos.strat = strat.name
        pos.sell_price = pos.strike
        pos.closed = timezone.now()
        pos.active = False
        pos.profit = round(
            (pos.sell_price - pos.buy_price) * amount_eth - (pos.sell_price + pos.buy_price) * amount_eth * 0.001, 2)
        pos.save()

        # Logs(text=f'закрыл позицию {pos.id, strat.name, pos.sell_price, pos.profit}').save()
    except:
        Logs(text=f' ошибка при закрытии позиции {pos.id, strat.name, pos.sell_price, pos.profit}').save()


def check_balance(strat, ):
    if strat.balance_usd - Position.objects.filter(strat=strat.name,
                                                   active=True).count() * strat.amount - strat.amount < 0:
        return False
    else:
        return True


def backtest_all(strats):
    # чищу базу
    ic('чищу базу')
    Position.objects.all().delete()
    Trades.objects.all().delete()

    list_markets = set(strats.values_list('exchange', 'pair'))
    # list_markets = (('kucoin','ETH/USDT'), ('kucoin','AXS/USDT'))
    currentPrices = {}

    # загружаю цены
    for market in list_markets:
        ic(market)
        if market[0] not in currentPrices:
            currentPrices[market[0]] = {}

        if True:

            currentPrices[market[0]].update(backtest.get_historical_price(market[0], market[1]))
        else:

            ic(f'ошибка в загрузке цен {market}')

    for strat in strats:

        # без котировки , переключаемся на след стратегию
        if strat.exchange in currentPrices:
            if strat.pair in currentPrices[strat.exchange]:
                prices = currentPrices[strat.exchange][strat.pair]
            else:
                continue
        else:
            continue

        # перебор котировок из dv_dict
        for price in prices:
            run_strat(strat, price['o'])
