def run():
    import os, django, sys

    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()

run()



from trader.models import Position, Tests, Variants, Strategies

from trader.view import store, indicators, g, back_perfom

from datetime import datetime

from icecream import ic

from django.db.models import Max

import json, statistics

import pandas as pd

from django_pandas.io import read_frame
import numpy as np



def calculate_analics():
    result = False

    df_positions = read_frame(
        Position.objects.filter(varian='AXS/USDT_ppv')
    ).sort_values('opened')

    start = df_positions.iloc[0].opened

    end = df_positions.iloc[-1].opened-1800000

    df = store.get_historical_price(type='all', start=start, end=end, exchange='binance', pair='AXS/USDT',
                                    timeframe='1m')
    df=df.set_index('timestamp')


    p2,p5,p10,p30, p60=[],[],[],[],[]

    for idx, position in df_positions.iterrows():
        try:
            p2.append(df.loc[position.opened+60000].close/position.buy_price)
            p5.append(df.loc[position.opened + 300000].close/position.buy_price)
            p10.append(df.loc[position.opened + 600000].close/position.buy_price)
            p30.append(df.loc[position.opened + 1800000].close/position.buy_price)
            p60.append(df.loc[position.opened + 3600000].close/position.buy_price)
        except:
            pass












    ic(len(p2),np.mean(p2))
    ic(len(p5), np.mean(p5))
    ic(len(p10), np.mean(p10))
    ic(len(p30), np.mean(p30))
    ic(len(p60), np.mean(p60))




    ic(result)
    return


if __name__=='__main__':
    calculate_analics()