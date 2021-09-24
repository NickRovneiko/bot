from trader.view import g, indicators, back_perfom, store, api, inform

from trader.models import Trades, Position, Logs, Options, Trans

from icecream import ic

from django.utils import timezone
import json

import pandas as pd

import telebot  # telegram

pd.options.display.max_columns = None


def execute_strat(d):
    d['positions'] = Position.objects.filter(varian=d['varian'], active=True)

    if not Options.objects.filter(varian=d['varian']).exists():
        # back_perfom.check_buy_option
        inform.me('BOT - нет опциона')
        exit()
        return
    else:
        if not d['positions'].exists():
            check_buy(d)
            return

        # проверка продажи

        check_sell(d)

        # проверка баланса
        if not check_balance(d):
            return

        # проверка покупки
        check_buy(d)

    return


def check_balance(d):
    if d['varian'].start_balance+sum(Trans.objects.filter(varian=d['varian']).values_list('amount', flat=True)) - d['amount']<= 0:
        return False
    else:
        return True


def check_sell(d):
    # проверка продажи
    if True:
        for row in d['positions']:
            if d['quote']['close'] > row.strike:
                back_perfom.try_sell(d,row)
                break
    else:
        Logs(text=f'ошибка в продаже {strat.name}').save()

    return


def check_buy(d):
    # проверка покупки
    if True:

        # если это первый ордер
        if not d['positions']:
            back_perfom.try_buy(d)
            return

        # покупаем если выше верхнего позиции + шага
        if d['quote']['close'] > d['positions'].order_by('buy_price').last().buy_price + d['step']:
            back_perfom.try_buy(d)
            return

        # покупаем если ниже нижней позиции + шага
        if d['quote']['close'] < d['positions'].order_by('buy_price').first().buy_price - d['step']:
            back_perfom.try_buy(d)

        # обновляем сумму шага
        # g.step = g.get_step(g.quote.open)

    else:
        Logs(text=f'ошибка в покупке{varian.name}').save()
    return


def validate_g_and_df(df: pd.DataFrame):
    df = df.dropna()

    return df


def graphs():
    return


def prepare_variables(d):
    settings=json.loads(d['varian'].settings)
    for key, value in settings.items():
        d[key]=value

    # догружаю переменные
    d['step'] = g.get_step(d)
    d['amount'] = d['varian'].start_balance / d['deals']
    return d


def run(df: pd.DataFrame, statistic=False):
    df = validate_g_and_df(df)

    for idx, price in df.iterrows():
        g.quote = price
        execute_strat()

    if not statistic:
        store.positions_save(g.df_positions.append(g.close_positions))
    g.varian.finish = True
    g.varian.save()


def run_online(varian=False):
    d = {}
    d['quote'] = api.get_quote(exchange=varian.exchange, pair=varian.pair)

    d['varian'] = varian
    d = prepare_variables(d)
    execute_strat(d)
