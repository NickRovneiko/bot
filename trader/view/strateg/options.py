from trader.view import g, indicators, back_perfom, store, api

from trader.models import Trades, Position, Logs, Options

from icecream import ic

from django.utils import timezone
import json

import pandas as pd
pd.options.display.max_columns = None



def execute_strat(varian='ETH/USDT_opt', quote=False):
    positions=Position.objects.filter(varian=varian)

    if not Options.objects.filter(varian=varian).exists():
        back_perfom.check_buy_option(varian=varian, quote=quote)
        return
    else:
        if not positions.exists():
            check_buy(positions=positions)
            return

        # проверка продажи
        check_sell()

        # проверка баланса
        if not check_balance():
            return

        # проверка покупки
        check_buy()

    return

def check_balance():
    if g.varian.start_balance - g.balance - g.amount <= 0:
        return False
    else:
        return True


def check_sell():
    # проверка продажи
    if True:
        for idx, row in g.df_positions.iterrows():
            if g.quote.open > row.strike:
                back_perfom.g_try_sell(row)

            else:
                break
    else:
        Logs(text=f'ошибка в продаже {strat.name}').save()

    return


def check_buy(positions=False, quote=False):
    # проверка покупки
    if True:

        # если это первый ордер
        if not positions:
            back_perfom.try_buy(quote)
            return

        # если пробила стоп и range-
        if quote.close > positions.order_by('buy_price').last().buy_price + 100:
            ic()
            back_perfom.try_buy()
            return

        # задним числом делаем закупку по лимитным ордерам
        i = 1
        while g.quote.open < (g.df_positions['buy_price'].iloc[0] - g.step * i):
            back_perfom.g_try_buy(price=g.df_positions['buy_price'].iloc[0] - g.step * i)
            i = i + 1
            if not check_balance() or not g.varian.limit_orders_buy:
                break
            return


        # покупаем если выше верхнего позиции + шага
        if g.quote.open > (g.df_positions['buy_price'].iloc[-1] + g.step):
            back_perfom.g_try_buy()


        # обновляем сумму шага

        g.step = g.get_step(g.quote.open)

    else:
        Logs(text=f'ошибка в покупке{varian.name}').save()
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

def run_online(varian=False):
    quote=api.get_quote(exchange=varian.exchange, pair=varian.pair)
    execute_strat(varian=varian, quote=quote)

