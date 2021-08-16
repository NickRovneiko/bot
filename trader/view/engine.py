from trader.models import Variants, Strategies, Position, History, Logs

from trader.view import store
from icecream import ic

import time





def attempt():
    strategies = Strategies.objects.all()

    for strat in strategies:
        if strat.status == 'Testing':
            backtesting_strategy(strat)


def backtesting_strategy(strat):
    # History.objects.all().delete()
    # Position.objects.all().delete()
    # Logs.objects.all().delete()



    varians = Variants.objects.filter(type=strat.variants)

    # запускаем для каждого варианта
    for varian in varians:
        start_time = time.time()

        start=1625097600000
        end=1629072000000



        df_prices = store.get_historical_price(exchange=varian.exchange, pair=varian.pair, start=start,end=end)
        df_positions = store.get_df_postions(varian.name)

        if len(df_positions) > 5:
            continue

        #импортирую стратегию
        from trader.view.Strateg import volat

        ic('запускаю стратегию')
        df_positions=volat.run(varian=varian, df_prices=df_prices,df_positions=df_positions)
        store.positions_save(df_positions)

        ic(f' времени заняло {round((time.time() - start_time))}')


def online():
    # достаем список бирж
    list_markets = set(varian.values_list('exchange', 'pair'))
    currentPrices = {}

def delete_varian(request):
    return
