from trader.models import Variants, Strategies, Position, History, Logs

from trader.view import store, g, varian_stats, indicators, analitics

from icecream import ic

import time
import datetime

import json


def online_bot():
    strategies = Strategies.objects.filter(status='Online')

    for strat in strategies:
        for varian in Variants.objects.filter(type=strat.name):
            g.get_strat_file(strat).run_online(varian)




def backtesting_strategy(strat):
    start = 1609459200000
    end = 1630454400000
    # timenow int(datetime.now().timestamp() * 1000

    for strat in Strategies.objects.all():
        g.strat = strat
        for varian in Variants.objects.filter(type=strat.variants, finish=False):


            # запускаем для каждого варианта
            start_time = time.time()
            df = store.get_historical_price(exchange=varian.exchange, pair=varian.pair, start=start, end=end)

            df = indicators.update_df_by_indicators(df)

            # задаю значение глобальных переменных
            g.varian = varian
            g.balance = varian.start_balance
            g.df_positions = store.get_df_postions(varian.name)
            g.close_positions = store.get_df_postions(varian.name, active=False)

            if g.strat.name == 'volat':
                # импортирую стратегию
                from trader.view.strateg import volat as strategy_file

                # догружаю переменные
                g.step = g.get_step(df.iloc[0].open)
                g.amount = varian.start_balance / varian.deals
                g.high_price = False


            g.get_strat_file(strat).run(df)

            ic(f' времени заняло {round((time.time() - start_time))}')


            if not varian.sharp and end-start>2629800000*2:
                ic(varian)
                ic(g.strat)
                varian_stats.get_detail_stats(varian)


def online():
    # достаем список бирж
    list_markets = set(varian.values_list('exchange', 'pair'))
    currentPrices = {}


def delete_varian(request):
    return
