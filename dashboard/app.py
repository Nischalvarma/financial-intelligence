import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

st.set_page_config(
    page_title="Quant Trading Dashboard",
    layout="wide"
)

# ====================================
# HEADER
# ====================================

st.title("Quant Trading Dashboard")

st.markdown("""
Machine Learning-Based Financial Analytics and Backtesting System
""")

# ====================================
# LOAD DATA
# ====================================

DATA_PATH = "data/processed"

files = os.listdir(DATA_PATH)

selected_file = st.sidebar.selectbox(
    "Select Stock",
    files
)

df = pd.read_csv(
    os.path.join(DATA_PATH, selected_file)
)

# ====================================
# METRICS
# ====================================

latest_close = df['Close'].iloc[-1]
latest_rsi = df['RSI'].iloc[-1]
latest_return = df['Returns'].iloc[-1]
latest_trend = df['Trend'].iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Close",
    f"{latest_close:.2f}"
)

col2.metric(
    "RSI",
    f"{latest_rsi:.2f}"
)

col3.metric(
    "Daily Return",
    f"{latest_return:.4f}"
)

col4.metric(
    "Trend",
    f"{latest_trend:.2f}"
)

# ====================================
# PRICE CHART
# ====================================

price_fig = go.Figure()

price_fig.add_trace(
    go.Scatter(
        y=df['Close'],
        mode='lines',
        name='Close Price'
    )
)

price_fig.add_trace(
    go.Scatter(
        y=df['SMA_10'],
        mode='lines',
        name='SMA 10'
    )
)

price_fig.add_trace(
    go.Scatter(
        y=df['SMA_50'],
        mode='lines',
        name='SMA 50'
    )
)

price_fig.update_layout(
    title="Price and Moving Averages",
    height=500
)

st.plotly_chart(
    price_fig,
    use_container_width=True
)

# ====================================
# RSI CHART
# ====================================

rsi_fig = go.Figure()

rsi_fig.add_trace(
    go.Scatter(
        y=df['RSI'],
        mode='lines',
        name='RSI'
    )
)

rsi_fig.update_layout(
    title="RSI Indicator",
    height=350
)

st.plotly_chart(
    rsi_fig,
    use_container_width=True
)

# ====================================
# SIGNALS
# ====================================

signals = pd.DataFrame()

signals['Close'] = df['Close']

signals['Signal'] = "HOLD"

signals.loc[
    (df['SMA_10'] > df['SMA_50']) &
    (df['RSI'] < 70),
    'Signal'
] = "BUY"

signals.loc[
    (df['SMA_10'] < df['SMA_50']) &
    (df['RSI'] > 30),
    'Signal'
] = "SELL"

st.subheader("Trading Signals")

st.dataframe(
    signals.tail(20),
    use_container_width=True
)

# ====================================
# RAW DATA
# ====================================

with st.expander("View Raw Dataset"):
    st.dataframe(
        df.tail(50),
        use_container_width=True
    )

# ====================================
# FOOTER
# ====================================

st.success("Dashboard Loaded Successfully")