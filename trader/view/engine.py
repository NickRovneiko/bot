from trader.models import Variants, Strategies, Position, History, Logs

from trader.view import store, g
from icecream import ic

import time
import datetime


def attempt():
    strategies = Strategies.objects.all()

    for strat in strategies:
        if strat.status == 'Testing':
            backtesting_strategy(strat)


def backtesting_strategy(strat):
    varians = Variants.objects.filter(type=strat.variants)

    # запускаем для каждого варианта
    for varian in varians:
        start_time = time.time()

        start = 1609459200000
        end = 1629072000000
        # timenow int(datetime.now().timestamp() * 1000

        df_prices = store.get_historical_price(exchange=varian.exchange, pair=varian.pair, start=start, end=end)



        # задаю значение глобальных переменных
        g.df_positions = store.get_df_postions(varian.name)
        g.close_positions = store.get_df_postions(varian.name, active=False)
        g.varian = varian
        g.step = g.get_step(df_prices.iloc[0].open)
        g.amount = varian.start_balance / varian.deals
        g.balance = varian.start_balance
        g.high_price = False

        if len(g.df_positions) > 5:
            continue

        # импортирую стратегию
        from trader.view.Strateg import volat

        ic('запускаю стратегию')
        volat.run(df_prices=df_prices)
        store.positions_save(g.df_positions.append(g.close_positions))

        ic(f' времени заняло {round((time.time() - start_time))}')


def online():
    # достаем список бирж
    list_markets = set(varian.values_list('exchange', 'pair'))
    currentPrices = {}


def delete_varian(request):
    return
