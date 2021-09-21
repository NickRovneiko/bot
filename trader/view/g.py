from icecream import ic

close_positions = False

df_positions = False

quote = False

step = False

varian = False

amount = False

balance = False

high_price = False

position = False  # отслеживала , открыта ли позициия. Это ускоряло с 41 до 38 секунд,  но выбивало иногда ошибку , неправильное было значение

strat = False

previous = False

options = False


def get_step(d):
    d['step'] = round(d['quote']['close'] * (d['range'] / 100) / d['deals'])
    return d['step']


def update_balance():
    balance = df_positions[df_positions['active'] == 1].count().active * amount
    return balance


def get_strat_file(strat=False):
    # компилятор python ругается
    if not strat:
        strategy_file = False

    if strat and strat.name == 'ma_cross':
        from trader.view.strateg import ma_cross as strategy_file

    if strat and strat.name == 'ppv':
        from trader.view.strateg import PPV as strategy_file

    if strat and strat.name == 'options':
        from trader.view.strateg import options as strategy_file

    return strategy_file
