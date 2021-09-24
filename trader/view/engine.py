from trader.models import Variants, Strategies

from trader.view import store, g, varian_stats, indicators, analitics

from icecream import ic

from django.utils import timezone
import datetime

import json

def online_bot():
    strategies = Strategies.objects.filter(status='Online')

    # проверяю есть ли текущий курс для варианта,  если нет то отправляю quote =False, чтоб грузил новые цены
    quote=False

    for strat in strategies:
        for varian in Variants.objects.filter(type=strat.name):
            if quote and varian.pair == quote['symbol']:
                g.get_strat_file(strat).run_online(varian=varian, quote=quote)

            else:
                quote = g.get_strat_file(strat).run_online(varian=varian, quote=False)





def backtesting_strategy(strat):
    start = 1609459200000
    end = 1630454400000
    # timenow int(datetime.now().timestamp() * 1000

    for strat in Strategies.objects.all():
        g.strat = strat
        for varian in Variants.objects.filter(type=strat.variants, finish=False):


            # запускаем для каждого варианта
            start_time = timezone.now()
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

            ic(f' времени заняло {round((timezone.now() - start_time))}')

            # если у стратегии нету шарпа и стратгеия работала больше 2 месцев
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
