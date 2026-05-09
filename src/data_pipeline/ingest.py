import yfinance as yf
import pandas as pd
from datetime import datetime
import os

print("🚀 Script started...")

# Ensure folder exists
os.makedirs("data/raw", exist_ok=True)

def fetch_stock_data(ticker):
    print(f"Fetching {ticker}...")

    df = yf.download(ticker, start="2020-01-01")

    if df.empty:
        print(f"❌ No data for {ticker}")
        return None

    df.reset_index(inplace=True)
    df['Ticker'] = ticker

    print(f"✅ Data fetched for {ticker}, rows: {len(df)}")
    return df


def save_to_csv(df, ticker):
    filename = f"data/raw/{ticker.replace('.', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"💾 Saved: {filename}")


if __name__ == "__main__":
    print("Running main...")

    tickers = ["RELIANCE.NS", "TCS.NS"]

    for ticker in tickers:
        df = fetch_stock_data(ticker)
        if df is not None:
            save_to_csv(df, ticker)

print("🎯 Script finished.")