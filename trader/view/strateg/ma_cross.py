from trader.view import g

from trader.models import Trades, Position, Logs

from icecream import ic

from django.utils import timezone

import pandas as pd

from decimal import Decimal

pd.options.display.max_columns = None


def execute_strat():
    # есть ли открытая позиция
    if not g.df_positions.empty:
        # если есть надо ли продавать
        if g.quote.slow > g.quote.fast:
            # продать
            try_sell()

    else:
        # надо ли покупать
        if g.quote.slow and g.quote.fast > g.quote.slow:
            try_buy()

    return


def try_buy(price=False):
    amount_base = g.balance / g.quote.open

    g.df_positions = g.df_positions.append({'varian': g.varian.name,
                                            'buy_price': g.quote.open,
                                            'opened': g.quote.timestamp,
                                            'amount_base': amount_base,
                                            'active': 1},
                                           ignore_index=True)
    g.balance = g.balance - amount_base * g.quote.open

    return


def try_sell():
    if len(g.df_positions) > 1:
        ic()
        ic('много позиций')
        ic(g.df_positions)
        ic(g.quote.timestamp)
        exit()
    elif len(g.df_positions) == 0:
        ic('отправили без позиции на продажу')
        ic(g.position)
        ic(g.df_positions)
        exit()


    row = g.df_positions.iloc[0]

    close_positions(row=row)

    # обновляю баланс и убираю комиссию
    g.balance = row.amount_base * g.quote.open - (row.sell_price + row.buy_price) * row.amount_base * 0.001

    return


def close_positions(row=False, stop=False):
    g.df_positions = g.df_positions.drop([row.name])

    # закрываю позицию
    row.sell_price = g.quote.open
    row.closed = g.quote.timestamp
    row.active = False
    row.profit = round(
        (row.sell_price - row.buy_price) * row.amount_base - (row.sell_price + row.buy_price) * row.amount_base * 0.001,
        6)

    # добавляю в базу выполненных позиций
    g.close_positions = g.close_positions.append(row)

    return
