import pandas as pd

from icecream import ic

close_positions = False

df_positions = False

quote = False

step = False

varian = False

amount = False

balance = False

high_price=False

position=False # отслеживала , открыта ли позициия. Это ускоряло с 41 до 38 секунд,  но выбивало иногда ошибку , неправильное было значение




def get_step(price):
    step = price * (varian.range / 100) / varian.deals
    return step


def update_balance():
    balance = df_positions[df_positions['active'] == 1].count().active * amount
    return balance
