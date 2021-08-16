from trader.view import api, backtest, store

from trader.models import Trades, Position, Logs

from icecream import ic

from django.utils import timezone

import pandas as pd

from decimal import Decimal

pd.options.display.max_columns = None


def execute_strat(varian, quote, df_positions):
    if df_positions.empty:
        df_positions = check_buy(varian, quote, df_positions)

    # проверка продажи
    df_positions = check_sell(varian, quote, df_positions)

    # проверка баланса
    if not check_balance(varian, df_positions):
        return df_positions

    # проверка покупки
    df_positions = check_buy(varian, quote, df_positions)

    return df_positions


def check_sell(varian, quote, df_positions):
    # проверка продажи
    if True:
        for idx, row in df_positions.iterrows():
            if quote.open > row.strike:
                df_positions = try_sell(quote, varian, row, df_positions)

            else:
                break
    else:
        Logs(text=f'ошибка в продаже {strat.name}').save()

    return df_positions


def check_buy(varian, quote, df_positions):
    # проверка покупки
    if True:

        # если это первый ордер
        if df_positions.empty:
            df_positions = try_buy(quote.open, varian, df_positions, quote)

            return df_positions

        # делаем задним числом  вставки на покупку вниз по стакану
        i = 1
        while quote.open < (df_positions['buy_price'].iloc[0] - varian.step * i):
            df_positions = try_buy(df_positions['buy_price'].iloc[0] - varian.step * i, varian, df_positions, quote)
            i = i + 1
            if not check_balance(varian, df_positions) or not varian.limit_orders_buy:
                break

        # делаем задним числом  вставки на покупку вверх по стакану

        i = 1
        while quote.open > (df_positions['buy_price'].iloc[-1] + varian.step * i):
            df_positions = try_buy(df_positions['buy_price'].iloc[-1] + varian.step * i, varian, df_positions, quote)
            i = i + 1
            if not check_balance(varian, df_positions) or not varian.limit_orders_buy:
                break

    else:
        Logs(text=f'ошибка в покупке{varian.name}').save()
    return df_positions


def try_buy(price, varian, df_positions, quote):
    amount_usd = round(varian.amount)
    amount_eth = round(varian.amount / price, 6)

    # Trades.objects.create(strat=varian.name,
    #                       types='BUY',
    #                       price=price,
    #                       amount_usd=-amount_usd,
    #                       amount_eth=amount_eth
    #                       )
    # # Logs(
    #     text=f'создал трейд {trade.id, strat.name} - "BUY"- {trade.price, -amount_usd, amount_eth,}').save()

    # открытие позиции
    df_positions = df_positions.append({'varian': varian.name,
                                        'buy_price': price,
                                        'strike': round(price + price * (varian.profit_percent / 100), 2),
                                        'opened': quote.timestamp,
                                        'amount_eth': amount_eth,
                                        'active': 1},
                                       ignore_index=True)

    # Logs(
    #     text=f'''создал позицию {position.id, position.strat, position.buy_price, position.strike, amount_eth}''').save()

    return df_positions


def try_sell(quote, varian, row, df_positions):
    amount_usd = round(row.amount_eth * quote.open, 2)
    amount_eth = row.amount_eth

    # Trades.objects.create(strat=strat.name,
    #                       types='SELL',
    #                       price=price,
    #                       amount_usd=amount_usd,
    #                       amount_eth=-amount_eth,
    #                       )
    # Logs(
    #     text=f'''создал трейд {trade.id, trade.strat} - "SELL"- {trade.price, amount_usd, -amount_eth}''').save()

    # закрытие позиции

    if True:

        pos = Position()
        pos.varian = varian.name
        pos.buy_price = row.buy_price
        pos.sell_price = row.strike
        pos.strike = row.strike
        pos.opened = row.opened
        pos.closed = quote.timestamp
        pos.active = False
        pos.profit = round(
            (pos.sell_price - row.buy_price) * amount_eth - (pos.sell_price + row.buy_price) * amount_eth * Decimal(
                0.001), 4)
        pos.save()

        df_positions = df_positions.drop([row.name])

        # Logs(text=f'закрыл позицию {pos.id, strat.name, pos.sell_price, pos.profit}').save()
    else:
        Logs(text=f' ошибка при закрытии позиции {pos.id, pos.name, pos.sell_price, pos.profit}').save()

    return df_positions


def check_balance(varian, df_positions):
    if varian.balance_usd - df_positions[
        df_positions['active'] == 1].count().active * varian.amount - varian.amount < 0:
        return False
    else:
        return True


# def backtest_all(strats):
#     # чищу базу
#     ic('чищу базу')
#     Position.objects.all().delete()
#     Trades.objects.all().delete()
#
#     list_markets = set(strats.values_list('exchange', 'pair'))
#     # list_markets = (('kucoin','ETH/USDT'), ('kucoin','AXS/USDT'))
#     currentPrices = {}
#
#     # загружаю цены
#     for market in list_markets:
#         ic(market)
#
#         if market[0] not in currentPrices:
#             currentPrices[market[0]] = {}
#
#         if True:
#
#             currentPrices[market[0]].update(backtest.get_historical_price(market[0], market[1]))
#         else:
#
#             ic(f'ошибка в загрузке цен {market}')
#
#     for strat in strats:
#
#         # без котировки , переключаемся на след стратегию
#         if strat.exchange in currentPrices:
#             if strat.pair in currentPrices[strat.exchange]:
#                 prices = currentPrices[strat.exchange][strat.pair]
#             else:
#                 continue
#         else:
#             continue
#
#         # перебор котировок из dv_dict
#         for price in prices:
#             run_strat(strat, price['o'])


def run(varian=False, df_prices=False, df_positions=False):
    for idx, price in df_prices.iterrows():

        df_positions = execute_strat(varian=varian, quote=price, df_positions=df_positions)
        df_positions = df_positions.sort_values('strike')


    return df_positions
