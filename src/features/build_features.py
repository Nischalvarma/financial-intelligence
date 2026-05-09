import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(__file__))
from indicators import add_all_indicators

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

def process_file(file):
    print(f"Processing {file}...")

    df = pd.read_csv(os.path.join(RAW_PATH, file))

    # numeric fix
    cols = ['Open','High','Low','Close','Volume']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')

    df.dropna(inplace=True)

    df = add_all_indicators(df)

    # lag features
    for col in ['RSI','MACD','Returns']:
        df[f"{col}_lag1"] = df[col].shift(1)
        df[f"{col}_lag2"] = df[col].shift(2)

    df.dropna(inplace=True)

    df.to_csv(os.path.join(PROCESSED_PATH, file), index=False)

if __name__ == "__main__":
    files = os.listdir(RAW_PATH)
    for f in files:
        process_file(f)

    print("✅ Features built")