import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = "data/processed"


def load_data():
    files = os.listdir(DATA_PATH)

    dfs = []

    for file in files:
        df = pd.read_csv(os.path.join(DATA_PATH, file))
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def prepare_data(df):

    df['Future_Close'] = df['Close'].shift(-5)

    df['Return_5d'] = (
        (df['Future_Close'] - df['Close']) / df['Close']
    )

    df['Target'] = 0

    df.loc[df['Return_5d'] > 0.02, 'Target'] = 1
    df.loc[df['Return_5d'] < -0.02, 'Target'] = -1

    df = df[df['Target'] != 0]

    df.dropna(inplace=True)

    features = [
        'SMA_10',
        'SMA_50',
        'RSI',
        'MACD',
        'MACD_Signal',
        'Returns',
        'Momentum_5',
        'Momentum_10',
        'Volatility_5',
        'Trend',
        'RSI_lag1',
        'RSI_lag2',
        'MACD_lag1',
        'MACD_lag2',
        'Returns_lag1',
        'Returns_lag2'
    ]

    X = df[features]
    y = df['Target']

    return X, y, df


def train_model(X, y, df):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=12,
        class_weight='balanced',
        random_state=42
    )

    model.fit(X_train, y_train)

    probs = model.predict_proba(X_test)

    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)

    baseline = y_test.value_counts(
        normalize=True
    ).max()

    print(f"Model Accuracy: {acc:.2f}")

    print(f"Baseline Accuracy: {baseline:.2f}")

    # BACKTESTING
    test_df = df.iloc[-len(y_test):].copy()

    confidence = probs.max(axis=1)

    test_df['Prediction'] = preds

    test_df['Confidence'] = confidence

    # Trade only if confidence > 0.60
    test_df['Trade'] = 0

    test_df.loc[
        test_df['Confidence'] > 0.75,
        'Trade'
    ] = test_df['Prediction']

    test_df['Strategy_Return'] = (
        test_df['Returns'] * test_df['Trade']
    )

    test_df['Cumulative'] = (
        1 + test_df['Strategy_Return']
    ).cumprod()

    print(
        f"Final Strategy Return: "
        f"{test_df['Cumulative'].iloc[-1]:.2f}"
    )

    print(
        "Trades taken:",
        (test_df['Trade'] != 0).sum()
    )


if __name__ == "__main__":

    print("🚀 Running model...")

    df = load_data()

    X, y, df = prepare_data(df)

    train_model(X, y, df)

    print("✅ Done")
