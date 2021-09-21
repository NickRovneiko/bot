from trader.models import Position, Tests, Variants, Strategies, Trans

from trader.view import store, indicators, g, back_perfom

from datetime import datetime

from icecream import ic

from django.db.models import Max

import json, statistics

import pandas as pd


def get_varian_stats(list_varian=False):
    list_varians = []

    for varian in list_varian:
        varian.open = Position.objects.filter(varian=varian.name, active=True).count()
        varian.closed = Position.objects.filter(varian=varian.name, active=False).count()
        varian.profit = sum(Position.objects.filter(varian=varian.name, active=False).values_list('profit', flat=True))
        varian.profit = round(varian.profit, 2) if varian.profit < 20 else round(varian.profit)

        varian.test_profit = Tests.objects.filter(name=varian.name).aggregate(Max('profit'))['profit__max']
        try:
            amount_in_open = Position.objects.filter(varian=varian.name, active=True).values_list('buy_price',
                                                                                                  'amount_base')
            summa = sum([position[0] * position[1] for position in amount_in_open])
            varian.balance = round(varian.start_balance + sum(Trans.objects.filter(varian=varian.name).values_list('amount', flat=True)) + varian.profit, 1)

            # по отношению к hold
            varian.if_hold = round(((varian.profit / varian.start_balance + 1) * 100) - Position.objects.filter(
                varian=varian.name).first().buy_price / Position.objects.filter(
                varian=varian.name).last().buy_price * 100 - 100)
            varian.hold = round(Position.objects.filter(
                varian=varian.name).first().buy_price / Position.objects.filter(
                varian=varian.name).last().buy_price * varian.start_balance, 2)

            varian.win_rate = round(
                Position.objects.filter(varian=varian.name, profit__gte=0).count() / Position.objects.filter(
                    varian=varian.name).count() * 100)

        except:
            pass

        if Position.objects.filter(varian=varian.name).exists():
            varian.opened = Position.objects.filter(varian=varian.name).order_by('opened').first().opened

        if Position.objects.filter(varian=varian.name).exists():
            varian.last = Position.objects.filter(varian=varian.name).order_by('opened').last().opened

        # if varian.balance > varian.amount:
        #     active_list_strats.append(varian)
        # else:
        #     stop_list_strats.append(varian)

        list_varians.append(varian)

    return list_varians


def get_detail_stats(varian=False):
    if not varian:
        varian = Variants.objects.get(name='AXS/USDT')

    positions = Position.objects.filter(varian=varian.name, active=False)

    # get prices
    from_unix = positions.last().opened
    till_unix = positions.first().closed

    df_prices = store.get_historical_price(exchange=varian.exchange, pair=varian.pair, start=from_unix, end=till_unix)

    g.strat = Strategies.objects.get(variants=varian.type)

    df_prices = indicators.update_df_by_indicators(df_prices)

    i = 0
    month_mili = 2629800000

    protit_by_30 = []



    from trader.view.strateg import PPV as strategy_file

    while from_unix + i * month_mili < till_unix:

        period_prices = df_prices.loc[
            (df_prices['timestamp'] >= from_unix + i * month_mili) & (
                    df_prices['timestamp'] <= from_unix + month_mili + i * month_mili)]

        period_prices=indicators.update_df_by_indicators(period_prices)

        # задаю значение глобальных переменных
        g.varian = varian
        g.balance = varian.start_balance
        g.df_positions = pd.DataFrame(columns=[column.name for column in Position._meta.get_fields()])
        g.close_positions = pd.DataFrame(columns=[column.name for column in Position._meta.get_fields()])


        # запуск стратегии
        g.get_strat_file(g.strat).run(df=period_prices, statistic=True)

        # закрываю позицию если открыта
        if len(g.df_positions) > 0:
            back_perfom.g_close_positions(g.df_positions.iloc[0])

        percent_profit = round(sum(g.close_positions['profit']) / varian.start_balance * 100)

        protit_by_30.append(percent_profit)

        i += 1

    try:
        standart_deviation = statistics.stdev(protit_by_30)
        average_profit_without_minus_risk = statistics.mean(protit_by_30) - len(protit_by_30)
        varian.sharp = round(average_profit_without_minus_risk / standart_deviation, 2)
    except:
        pass


    # сохраняю статистику в varian
    # месячная доходность в процентах
    varian.month_profit = round(statistics.mean(protit_by_30))
    varian.average_profit = protit_by_30
    varian.save()

    return
