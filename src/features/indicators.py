import pandas as pd

def add_moving_averages(df):
    df['SMA_10'] = df['Close'].rolling(10).mean()
    df['SMA_50'] = df['Close'].rolling(50).mean()
    return df

def add_rsi(df, window=14):
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(window).mean()
    loss = -delta.clip(upper=0).rolling(window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def add_macd(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    return df

def add_bollinger(df):
    sma = df['Close'].rolling(20).mean()
    std = df['Close'].rolling(20).std()
    df['BB_Upper'] = sma + 2*std
    df['BB_Lower'] = sma - 2*std
    return df

def add_returns(df):
    df['Returns'] = df['Close'].pct_change()
    return df

def add_momentum(df):
    df['Momentum_5'] = df['Close'].pct_change(5)
    df['Momentum_10'] = df['Close'].pct_change(10)
    return df

def add_volatility(df):
    df['Volatility_5'] = df['Returns'].rolling(5).std()
    return df

def add_trend(df):
    df['Trend'] = df['SMA_10'] - df['SMA_50']
    return df

def add_all_indicators(df):
    df = add_moving_averages(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_bollinger(df)
    df = add_returns(df)
    df = add_momentum(df)
    df = add_volatility(df)
    df = add_trend(df)
    return df