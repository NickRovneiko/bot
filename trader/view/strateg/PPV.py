from trader.view import g, indicators, back_perfom, store

from trader.models import Trades, Position, Logs

from icecream import ic

from django.utils import timezone
import json

import pandas as pd
pd.options.display.max_columns = None



def execute_strat():
    # есть ли открытая позиция
    if not g.df_positions.empty:
        # если есть надо ли продавать
        if g.quote.close < g.quote.bottom_band:
            # продать
            back_perfom.g_try_sell()

    else:
        # надо ли покупать
        if g.quote.close > g.quote.upper_band:
            if g.previous:
                back_perfom.g_try_buy()
            else:
                g.previous=True

        else:
            g.previous=False

    return

def validate_g_and_df(df:pd.DataFrame):
    df=df.dropna()



    return df


def graphs():

    return


def run(df:pd.DataFrame, statistic=False):
    df=validate_g_and_df(df)

    for idx, price in df.iterrows():
        g.quote = price
        execute_strat()

    if not statistic:
        store.positions_save(g.df_positions.append(g.close_positions))
    g.varian.finish = True
    g.varian.save()
