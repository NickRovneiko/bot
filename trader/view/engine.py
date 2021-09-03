from trader.models import Variants, Strategies, Position, History, Logs

from trader.view import store, g, varian_stats,indicators

from icecream import ic

import time
import datetime

import json


def attempt():
    strategies = Strategies.objects.all()

    for strat in strategies:
        if strat.status == 'Testing':
            backtesting_strategy(strat)


def backtesting_strategy(strat):
    start = 1617235200000
    end = 1629072000000
    # timenow int(datetime.now().timestamp() * 1000

    for g.strat in Strategies.objects.all():
        for varian in Variants.objects.filter(type=strat.variants, finish=False):


            # запускаем для каждого варианта
            start_time = time.time()
            df= store.get_historical_price(exchange=varian.exchange, pair=varian.pair, start=start, end=end)

            df=indicators.update_df_by_indicators(df)


            # задаю значение глобальных переменных
            g.varian = varian
            g.balance = varian.start_balance
            g.df_positions = store.get_df_postions(varian.name)
            g.close_positions = store.get_df_postions(varian.name, active=False)


            if strat.name == 'volat':
                # импортирую стратегию
                from trader.view.strateg import volat as strategy_file

                # догружаю переменные
                g.step = g.get_step(df.iloc[0].open)
                g.amount = varian.start_balance / varian.deals
                g.high_price = False


            if strat.name == 'ma_cross':
                from trader.view.strateg import ma_cross as strategy_file




            for idx, price in df.iterrows():
                g.quote = price

                strategy_file.execute_strat()

            store.positions_save(g.df_positions.append(g.close_positions))
            varian.finish=True
            varian.save()

            ic(f' времени заняло {round((time.time() - start_time))}')

        for varian in Variants.objects.filter(type=strat.variants):
            if not varian.sharp:
                varian_stats.get_detail_stats(varian)



def online():
    # достаем список бирж
    list_markets = set(varian.values_list('exchange', 'pair'))
    currentPrices = {}


def delete_varian(request):
    return
