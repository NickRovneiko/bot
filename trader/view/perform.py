from trader.models import Trades, Position, Logs

from icecream import ic

from django.utils import timezone

import pandas as pd

pd.options.display.max_columns = None


def try_buy(price=False):
    amount_base = g.balance / g.quote.close

    g.df_positions = g.df_positions.append({'varian': g.varian.name,
                                            'buy_price': g.quote.close,
                                            'opened': g.quote.timestamp,
                                            'amount_base': amount_base,
                                            'active': 1},
                                           ignore_index=True)
    g.balance = g.balance - amount_base * g.quote.close

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
    g.balance = row.amount_base * g.quote.close - (row.sell_price + row.buy_price) * row.amount_base * 0.001

    return


def close_positions(row=False, stop=False):
    g.df_positions = g.df_positions.drop([row.name])

    # закрываю позицию
    row.sell_price = g.quote.close
    row.closed = g.quote.timestamp
    row.active = False
    row.profit = round(
        (row.sell_price - row.buy_price) * row.amount_base - (row.sell_price + row.buy_price) * row.amount_base * 0.001,
        6)

    # добавляю в базу выполненных позиций
    g.g_close_positions = g.g_close_positions.append(row)

    return


def buy_option():
    return