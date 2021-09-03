def server():
    import os, django, sys

    project_home = '/home/drann/bot'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'bot.settings'
    django.setup()


server()

from django_pandas.io import read_frame

from trader.models import History

from icecream import ic

pair = 'ETH/USDT'
qs = History.objects.filter(exchange='binance',
                            pair=pair,
                            timestamp__gte=1609459200000,
                            timeframe='1m',
                            ).exclude(timestamp__gte=1629072000000)
df_prices = read_frame(qs)















import plotly.graph_objects as go

fig = go.Figure([go.Scatter(x=df['Date'], y=df['AAPL.High'])])

fig.show()
