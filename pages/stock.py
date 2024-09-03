# stock_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate daily returns
def calculate_daily_returns(df):
    df['daily_return'] = df['close'].pct_change() * 100
    return df

# Streamlit dashboard for stock data
st.title('Stock Data Dashboard')

# Upload CSV file
uploaded_stock_file = st.file_uploader("Upload your stock data CSV file", type=["csv"])

if uploaded_stock_file is not None:
    # Load data
    stock_df = pd.read_csv(uploaded_stock_file)

    # Display data
    st.write("### Stock Data")
    st.write(stock_df.head())

    # Ensure necessary columns are present
    if 'date' in stock_df.columns and 'close' in stock_df.columns:
        # Convert date column to datetime
        stock_df['date'] = pd.to_datetime(stock_df['date'])
        stock_df.set_index('date', inplace=True)

        # Calculate daily returns
        stock_df = calculate_daily_returns(stock_df)

        # Display data with daily returns
        st.write("### Data with Daily Returns")
        st.write(stock_df.head())

        # Plot daily returns
        st.write("### Daily Returns Plot")
        plt.figure(figsize=(10, 5))
        plt.plot(stock_df.index, stock_df['daily_return'], label='Daily Return (%)')
        plt.xlabel('Date')
        plt.ylabel('Daily Return (%)')
        plt.title('Daily Stock Returns')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.error("The CSV file must contain 'date' and 'close' columns.")
