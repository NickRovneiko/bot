from trader.view import g, back_perfom, store

from trader.models import Trades, Position, Logs

from icecream import ic

from django.utils import timezone

import pandas as pd

from decimal import Decimal

pd.options.display.max_columns = None


def execute_strat():

    if not g.options or g.options.a:

        # Options.objects.filter(varian=d['varian']).exists():
        back_perfom.check_buy_option

        return
    else:
        if g.df_positions.empty:
            check_buy()
            return

        # проверка продажи
        check_sell()

        # проверка баланса
        if not check_balance():
            return

        # проверка покупки
        check_buy()

    return

def check_sell():
    # проверка продажи
    if True:
        for idx, row in g.df_positions.iterrows():
            if g.quote.open > row.strike:
                try_sell(row)

            else:
                break
    else:
        Logs(text=f'ошибка в продаже {strat.name}').save()

    return


def check_buy():
    # проверка покупки
    if True:

        # если это первый ордер
        if g.df_positions.empty:
            try_buy()
            return

        # если пробила стоп и range
        if 100 - g.quote.open / g.high_price.buy_price*100 - 5 > g.varian.range:
            try_buy()
            return

        # задним числом делаем закупку по лимитным ордерам
        i = 1
        while g.quote.open < (g.df_positions['buy_price'].iloc[0] - g.step * i):
            try_buy(price=g.df_positions['buy_price'].iloc[0] - g.step * i)
            i = i + 1
            if not check_balance() or not g.varian.limit_orders_buy:
                break
            return


        # покупаем если выше верхнего позиции + шага
        if g.quote.open > (g.df_positions['buy_price'].iloc[-1] + g.step):
            try_buy()


        # обновляем сумму шага

        g.step = g.get_step(g.quote.open)

    else:
        Logs(text=f'ошибка в покупке{varian.name}').save()
    return


def try_buy(price=False):
    if not price:
        price=g.quote.open

    amount_base = g.amount / price

    g.df_positions = g.df_positions.append({'varian': g.varian.name,
                                            'buy_price': price,
                                            'strike': round(price + price * (g.varian.profit_percent / 100), 8),
                                            'opened': g.quote.timestamp,
                                            'amount_base': amount_base,
                                            'active': 1},
                                           ignore_index=True)

    g.df_positions = g.df_positions.sort_values('strike')
    g.balance = g.update_balance()
    g.high_price = g.df_positions.nlargest(1, 'buy_price').iloc[0]

    # Logs(
    #     text=f'''создал позицию {position.id, position.strat, position.buy_price, position.strike, amount_base}''').save()

    return


def try_sell(row):
    close_positions(row=row)

    # Trades.objects.create(strat=strat.name,
    #                       types='SELL',
    #                       price=price,
    #                       amount_usd=amount_usd,
    #                       amount_eth=-amount_eth,
    #                       )
    # Logs(
    #     text=f'''создал трейд {trade.id, trade.strat} - "SELL"- {trade.price, amount_usd, -amount_eth}''').save()

    # закрытие позиции

    # Logs(text=f'закрыл позицию {pos.id, strat.name, pos.sell_price, pos.profit}').save()
    # else:
    #     Logs(text=f' ошибка при закрытии позиции {pos.id, pos.name, pos.sell_price, pos.profit}').save()

    return


def check_balance():
    if g.varian.start_balance - g.balance - g.amount <= 0:
        if g.varian.stop_loss:
            stop_loss()

        return False
    else:
        return True


def close_positions(row=False, stop=False):
    g.df_positions = g.df_positions.drop([row.name])

    if stop:
        row.strike = g.quote.open

    # закрываю позицию
    row.sell_price = row.strike
    row.closed = g.quote.timestamp
    row.active = False
    row.profit = round(
        (row.sell_price - row.buy_price) * row.amount_base - (row.sell_price + row.buy_price) * row.amount_base * 0.001,
        6)

    g.close_positions = g.close_positions.append(row)
    g.balance = g.update_balance()

    return


def validate_g_and_df(df: pd.DataFrame):
    df = df.dropna()

    return df


def graphs():
    return


def update_variables():
    g.step = g.get_step(g.quote.close)
    g.amount = g.varian.start_balance / g.varian.deals


def run_back(df_prices=False, statistic=False):
    df_prices = validate_g_and_df(df_prices)


    for idx, price in df_prices.iterrows():
        g.quote = price
        ic(g.quote)

        update_variables()
        execute_strat()

    if not statistic:
        store.positions_save(g.df_positions.append(g.close_positions))
    g.varian.finish = True
    g.varian.save()

    return

