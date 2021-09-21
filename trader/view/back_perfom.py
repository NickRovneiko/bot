from trader.view import g, api

from trader.models import Trades, Position, Logs, Options, Trans

from icecream import ic

from django.utils import timezone

from datetime import timedelta

import pandas as pd

pd.options.display.max_columns = None


def g_try_buy(price=False):
    amount_base = g.balance / g.quote.close

    g.df_positions = g.df_positions.append({'varian': g.varian.name,
                                            'buy_price': g.quote.close,
                                            'opened': g.quote.timestamp,
                                            'amount_base': amount_base,
                                            'active': 1},
                                           ignore_index=True)
    g.balance = g.balance - amount_base * g.quote.close

    return


def g_try_sell():
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

    g_close_positions(row=row)

    # обновляю баланс и убираю комиссию
    g.balance = row.amount_base * g.quote.close - (row.sell_price + row.buy_price) * row.amount_base * 0.001

    return


def g_close_positions(row=False, stop=False):
    g.df_positions = g.df_positions.drop([row.name])

    # закрываю позицию
    row.sell_price = g.quote.close
    row.closed = g.quote.timestamp
    row.active = False
    row.profit = round(
        (row.sell_price - row.buy_price) * row.amount_base - (row.sell_price + row.buy_price) * row.amount_base * 0.001,
        6)

    # добавляю в базу выполненных позиций
    g.close_positions = g.close_positions.append(row)

    return


def check_buy_option(d):
    strike = int(((d['quote']['close'] // 50) + 1) * 50)
    expiration_2day = (timezone.now().date() + timedelta(days=2)).strftime('%d%b%y').upper()
    expiration_1day = (timezone.now().date() + timedelta(days=1)).strftime('%d%b%y').upper()

    try:
        # ETH-18SEP21-3600-P
        result = api.get_quote(exchange=d['varian'].exchange, pair=f'ETH-{expiration_2day}-{strike}-P')
        expiration = timezone.now() + timedelta(days=2)
    except:
        result = api.get_quote(exchange=d['varian'].exchange, pair=f'ETH-{expiration_1day}-{strike}-P')
        expiration = timezone.now() + timedelta(days=1)

    if result['ask'] * d['quote']['close'] < 80:
        # виртуальная покупка опицона
        price = result['ask'] * d['quote']['close']
    else:
        return

    Options(varian=d['varian'].name,
            buy_price=price,
            strike=strike,
            expiration=expiration,
            amount=1).save()



    return


def try_buy(d, strike=False):
    amount_base = d['amount'] / d['quote']['close']

    strike = d['quote']['close'] * (1 + d['strike']/100)

    Position(varian=d['varian'].name,
             buy_price=d['quote']['close'],
             strike=strike,
             opened=d['quote']['datetime'],
             amount_base=amount_base,
             active=True).save()

    Trans(varian=d['varian'].name,
          amount=-d['amount'],
          desc=f"покупка по {d['quote']['close']}").save()

    return d
def try_sell(d, row):

    row.sell_price = d['quote']['close']
    row.closed = timezone.now()
    row.active = False
    row.profit = (row.sell_price-row.buy_price) * row.amount_base-(row.sell_price + row.buy_price) * row.amount_base * 0.0005
    row.save()

    Trans(varian = d['varian'].name,
          amount = (row.sell_price-row.buy_price) * row.amount_base,
          desc=f"продажа по {d['quote']['close']}").save()

    return