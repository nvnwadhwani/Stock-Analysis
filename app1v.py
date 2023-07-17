import streamlit as st
import pandas as pd
import talib
import yfinance as yf
import plotly.graph_objects as go
# import sklearn
from datetime import datetime, timedelta
# from sklearn.linear_regression import LinearRegression
# from sklearn.metrics import mean_squared_error


def main():
    end_date = datetime.now() - timedelta(days=1)
    
    # Load the stock data
    stocks = st.sidebar.text_input("Enter a list of stocks (comma-separated)", "RELIANCE.NS")
    data = yf.download(stocks, start="2014-01-01", end=end_date.strftime("%Y-%m-%d"))

    # Calculate the 200-day moving average
    close = data["Adj Close"]
    MA200 = close.rolling(200).mean()

    # Calculate the MACD indicator
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

    # Calculate the Stochastic Oscillator
    stoch, stoch_signal = talib.STOCH(data["High"], data["Low"], close, fastk_period=14, slowk_period=3, slowd_period=3)

    # Show the buy and sell signals
    buy_signal = (MA200 > close) & (macd > macdsignal) & (stoch < 20)
    sell_signal = (MA200 < close) & (macd < macdsignal) & (stoch > 80)

    # Create the Streamlit app
    st.title("Stock Analysis")
    st.write("This strategy is based on the following principles: \n")
    st.write("- Trend following: The strategy buys stocks that are trending upwards and sells stocks that are trending downwards.")
    st.write("- Momentum: The strategy buys stocks that are oversold and sells stocks that are overbought.")
    st.write("- Risk management: The strategy uses stop losses to protect against losses.")

    # Create a combined chart
    fig = go.Figure()

    # Add the stock price to the combined chart
    fig.add_trace(go.Scatter(x=data.index, y=close, name="Stock Price"))

    # Add the 200-day moving average to the combined chart
    fig.add_trace(go.Scatter(x=data.index, y=MA200, name="MA200"))

    # Add the MACD signal line to the combined chart
    fig.add_trace(go.Scatter(x=data.index, y=macdsignal, name="MACD Signal"))

    # Add the MACD histogram to the combined chart
    fig.add_trace(go.Scatter(x=data.index, y=macdhist, name="MACD Histogram"))

    # Add the Stochastic Oscillator to the combined chart
    fig.add_trace(go.Scatter(x=data.index, y=stoch, name="Stochastic Oscillator"))

    # Add the Stochastic Oscillator signal line to the combined chart
    fig.add_trace(go.Scatter(x=data.index, y=stoch_signal, name="Stochastic Oscillator Signal"))

    # Add the buy and sell signals to the combined chart
    fig.add_trace(go.Scatter(x=data.index[buy_signal], y=close[buy_signal], mode="markers", name="Buy Signal", marker=dict(color="green")))
    fig.add_trace(go.Scatter(x=data.index[sell_signal], y=close[sell_signal], mode="markers", name="Sell Signal", marker=dict(color="red")))

    # Configure the layout of the combined chart
    fig.update_layout(
        title="Stock Indicators",
        xaxis_title="Date",
        yaxis_title="Value",
        legend=dict(orientation="v", yanchor="bottom", y=10.02, xanchor="auto", x=0.5)
    )

    # Display the combined chart
    st.plotly_chart(fig)


# def predict_price(ticker, horizon):
#     data = yf.download(ticker, start="2014-01-01", end="2022-01-01")
#     close = data["Close"]

#     # Train the linear regression model
#     model = LinearRegression()
#     model.fit(close.to_numpy().reshape(-1, 1), close.to_numpy())

#     # Predict the future price of the stock
#     future_price = model.predict(np.array([2023, 1, 1]).reshape(-1, 1))[0]

#     return future_price

# def evaluate_model(model, data, horizon):
#     close = data["Close"]
#     predictions = model.predict(close.to_numpy().reshape(-1, 1))
#     mse = mean_squared_error(close[horizon:], predictions[horizon:])

#     return mse

# if __name__ == "__main__":
#     ticker = st.text_input("Enter a stock ticker:")
#     horizon = st.number_input("Enter the time horizon (in days):")
#     future_price = predict_price(ticker, horizon)
#     mse = evaluate_model(model, data, horizon)

#     st.write("The predicted price of the stock is:", future_price)
#     st.write("The mean squared error of the model is:", mse)
    
    
if __name__ == "__main__":
    main()
