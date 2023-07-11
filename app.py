import streamlit as st
import pandas as pd
import yfinance as yf
import talib


# Set the title and subtitle of the app
st.title("Portfolio Analysis App")
st.subheader("NSE India")

# Create a sidebar for user input
st.sidebar.title("Parameters")
stocks = st.sidebar.text_input("Enter a list of stocks (comma-separated)", "AAPL, GOOGL, MSFT")
rsi_threshold = st.sidebar.slider("RSI Threshold", 0, 100, 30)
ma_200_threshold = st.sidebar.number_input("200-day MA Threshold", value=0)
ma_50_threshold = st.sidebar.number_input("50-day MA Threshold", value=0)

# Fetch stock data from Yahoo Finance
@st.cache_data
def load_data(tickers):
    data = yf.download(tickers, start="2022-01-01", end="2022-12-31")["Adj Close"]
    return data

# Load data for the selected stocks
stock_data = load_data([stock.strip() for stock in stocks.split(",")])

# Calculate technical indicators (RSI, 200-day MA, 50-day MA)
rsi = talib.RSI(stock_data, timeperiod=20)
ma_200 = talib.SMA(stock_data, timeperiod=200)
ma_50 = talib.SMA(stock_data, timeperiod=50)

# Display stock data and analysis
for stock in stock_data.columns:
    st.subheader(stock)
    st.line_chart(stock_data[stock])
    st.subheader("Technical Indicators")
    st.line_chart(rsi[stock])
    st.line_chart(ma_200[stock])
    st.line_chart(ma_50[stock])

    # Check trading conditions
    last_rsi = rsi[stock][-1]
    last_ma_200 = ma_200[stock][-1]
    last_ma_50 = ma_50[stock][-1]

    if last_rsi > rsi_threshold and last_ma_200 > ma_200_threshold and last_ma_50 > ma_50_threshold:
        st.success("Trading Signal: Buy")
        # Plot buy signal
        buy_signal_df = pd.DataFrame(stock_data[stock])
        buy_signal_df["Buy Signal"] = buy_signal_df[stock].where(
            (rsi[stock] > rsi_threshold) &
            (ma_200[stock] > ma_200_threshold) &
            (ma_50[stock] > ma_50_threshold),
            None
        )
        st.line_chart(buy_signal_df)

    else:
        st.warning("Trading Signal: Sell")
        # Plot sell signal
        sell_signal_df = pd.DataFrame(stock_data[stock])
        sell_signal_df["Sell Signal"] = sell_signal_df[stock].where(
            (rsi[stock] <= rsi_threshold) |
            (ma_200[stock] <= ma_200_threshold) |
            (ma_50[stock] <= ma_50_threshold),
            None
        )
        st.line_chart(sell_signal_df)

