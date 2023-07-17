import streamlit as st
import pandas as pd
import talib
import yfinance as yf

def main():
    # Load the stock data
    ticker = st.text_input("Enter the stock ticker:")
    data = yf.download(ticker, start="2022-01-01", end="2023-01-01")

    # Calculate the 200-day moving average
    close = data["Close"]
    MA200 = close.rolling(200).mean()

    # Calculate the MACD indicator
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    # Calculate the Stochastic Oscillator
    stoch = talib.STOCH(close, high=data["High"], low=data["Low"], fastkperiod=14, slowkperiod=3, slowdperiod=3)

    # Create the Streamlit app
    st.title("Stock Investment Strategy")

    # Plot the stock price
    st.line_chart(close)

    # Plot the 200-day moving average
    st.line_chart(MA200)

    # Plot the MACD indicator
    st.line_chart(macd)
    st.line_chart(macdsignal)
    st.line_chart(macdhist)

    # Plot the Stochastic Oscillator
    st.line_chart(stoch["K"])
    st.line_chart(stoch["D"])

    # Show the buy and sell signals
    buy_signal = MA200 > close and macd > macdsignal and stoch["K"] < 20
    sell_signal = MA200 < close and macd < macdsignal and stoch["K"] > 80

    st.write("Buy signal:", buy_signal)
    st.write("Sell signal:", sell_signal)

if __name__ == "__main__":
    main()
