def server():
    import os, django, sys

    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()


server()

from django_pandas.io import read_frame
import pandas as pd
import numpy as np

pd.options.display.max_columns = None

from trader.models import History
from icecream import ic

import math

pair = 'AXS/USDT'
start = 1625097600000

qs = History.objects.filter(exchange='binance',
                            pair=pair,
                            timestamp__gte=start,
                            timeframe='1m',
                            ).exclude(timestamp__gte=1629072000000)
df = read_frame(qs)

df['ts'] = pd.to_datetime(df['timestamp'], unit='ms')

period = f"{df.ts.dt.date.iloc[0]} - {df.ts.dt.date.iloc[-1]}"

df['minute'] = df.ts.dt.minute

# волатильность по close из n предыдущей котировки
timeframe_minute = 15
df['volat'] = df.high.rolling(window=timeframe_minute).max() / df.low.rolling(window=timeframe_minute).min() * 100 - 100

# ic(df[['low','high', 'volat']][-60:])


# продолжение движения цены
df['continue_move'] = ((df.close - df.open) / df.open) * ((df.close.shift(1) - df.open.shift(1)) / df.open.shift(1))
df['continue_move'] = abs(df.continue_move.apply(np.ceil))
# ic(df[['open','close', 'continue_move']][:20])


df = df.dropna()

agg_func_math = {
    'volat': ['mean', 'std'],
}

# группирую
df_min = df.groupby('minute').agg(agg_func_math)

# удаляю мультиииндекс
df_min.columns = df_min.columns.droplevel(0)

df_min = df_min.reset_index()

import plotly.graph_objects as go
import plotly.express as px

fig = px.line(df_min, x='minute', y=df_min.columns, title=f'{pair} - {period}')



# старт Y c нуля
fig.update_yaxes(rangemode="tozero")

fig.show()
