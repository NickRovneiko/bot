def server():
    import os, django, sys

    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()


server()

from trader.models import Variants, Position, History, Tests, Strategies

from icecream import ic

from datetime import datetime

from trader.view import store, indicators, g

from trader.view.strateg import ma_cross as strategy_file

import random

import pandas as pd

from django_pandas.io import read_frame

import json


def start():
    for varian in Variants.objects.filter(type='ma_cross'):
        run(varian)


def run(varian=False):
    # запускаем для каждого варианта
    qs = History.objects.filter(exchange=varian.exchange,
                                pair=varian.pair,
                                timestamp__gte=1609459200000,
                                timeframe='1m',
                                ).exclude(timestamp__gte=1629072000000)
    df_prices = read_frame(qs)
    df_prices = df_prices[['timestamp', 'open']]
    while Tests.objects.filter(name=varian.name).count() < 130:

        fast = random.randint(1, 30000)
        slow = random.randint(fast, 60000)

        # prepare indicator for strategy
        df = indicators.ma(df_prices, name='fast', period=fast)
        df = indicators.ma(df, name='slow', period=slow)
        indics = f'fast: {fast}, slow: {slow}'

        # задаю значение глобальных переменных
        g.varian = varian
        g.balance = varian.start_balance
        g.df_positions = pd.DataFrame(columns=[column.name for column in Position._meta.get_fields()])
        g.close_positions = g.df_positions

        for idx, price in df.iterrows():
            g.quote = price

            strategy_file.execute_strat()

        win_rate = round(len(g.close_positions[g.close_positions['profit'] > 0]) / len(g.close_positions) * 100)
        profit = round(g.close_positions['profit'].sum(), 2)
        ic(win_rate, profit)

        store.test_save(varian=varian, win_rate=win_rate, profit=profit, text=indics)

        # time.sleep(30)


start()
