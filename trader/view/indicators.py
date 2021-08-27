import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from ta.volatility import BollingerBands, DonchianChannel




def ma(df, name=False, period=False):
    df[name] = df.iloc[:, 1].rolling(window=period).mean()

    return df
def bollinger(df):
    indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)

    df['bb_bbm'] = indicator_bb.bollinger_mavg()
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    return df

def dochian(df):


    indicator_doc= DonchianChannel(close=df["close"],high=df['high'], low=df['low'], window=10)
    df['doc_h'] = indicator_doc.donchian_channel_hband()
    df['doc_l'] = indicator_doc.donchian_channel_lband()



    return df



