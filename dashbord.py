import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import pynance as pn

# Function to calculate RSI
def calculate_rsi(data, window):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Streamlit app
st.title("Stock Price Analysis Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload your stock data CSV file", type=["csv"])

if uploaded_file is not None:
    # Load your stock price data
    df = pd.read_csv(uploaded_file)

    # Ensure your data includes columns like Open, High, Low, Close, and Volume
    st.write("Data Preview")
    st.dataframe(df.head())

    # Calculate moving averages
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    # Calculate RSI (Relative Strength Index)
    df['RSI'] = calculate_rsi(df['Close'], 14)

    # Calculate Sharpe Ratio manually
    returns = df['Close'].pct_change().dropna()
    mean_return = returns.mean()
    std_return = returns.std()
    sharpe_ratio = mean_return / std_return * np.sqrt(252)  # Annualizing the Sharpe Ratio
    st.write(f'Sharpe Ratio: {sharpe_ratio:.2f}')

    # Set the style for plots
    sns.set(style="whitegrid")

    # Plot the stock price and moving averages
    st.write("Stock Price and Moving Averages")
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df['Close'], label='Close Price', color='blue')
    ax.plot(df['SMA_50'], label='50-Day SMA', color='red')
    ax.plot(df['SMA_200'], label='200-Day SMA', color='green')
    ax.set_title('Stock Price and Moving Averages')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    st.pyplot(fig)

    # Plot RSI
    st.write("Relative Strength Index (RSI)")
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df['RSI'], label='RSI', color='purple')
    ax.set_title('Relative Strength Index (RSI)')
    ax.set_xlabel('Date')
    ax.set_ylabel('RSI')
    ax.legend()
    st.pyplot(fig)
else:
    st.write("Please upload a CSV file to analyze the stock data.")
