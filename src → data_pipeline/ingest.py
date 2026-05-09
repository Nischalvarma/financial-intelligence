import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Ensure data directory exists
os.makedirs("data/raw", exist_ok=True)

def fetch_stock_data(ticker="RELIANCE.NS", start="2020-01-01", end=None):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')

    print(f"Fetching data for {ticker}...")

    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        print(f"No data found for {ticker}")
        return None

    df.reset_index(inplace=True)
    df['Ticker'] = ticker

    return df


def save_to_csv(df, ticker):
    filename = f"data/raw/{ticker.replace('.', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved data to {filename}")


if __name__ == "__main__":
    tickers = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS"
    ]

    for ticker in tickers:
        df = fetch_stock_data(ticker)

        if df is not None:
            save_to_csv(df, ticker)