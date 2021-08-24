



def ma(df, name=False, period=False):
    df[name] = df.iloc[:, 1].rolling(window=period).mean()

    return df