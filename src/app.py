import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import tkinter as tk
    from tkinter import filedialog
except ImportError:
    tk = None

import pynance as pn

# Function to open a file dialog and return the selected file path
def upload_file():
    if tk is not None:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file_path = filedialog.askopenfilename(
            title="Select your stock data file",
            filetypes=[("CSV files", "*.csv")]
        )
    else:
        print("tkinter is not available. Please provide the file path manually.")
        file_path = input("Enter the path to your stock data CSV file: ")
    return file_path

# Load the file using the file dialog or manual input
file_path = upload_file()

if not file_path:
    print("No file selected. Exiting.")
    exit()

# Load your stock price data
df = pd.read_csv(file_path)

# Ensure your data includes columns like Open, High, Low, Close, and Volume
print(df.head())

# Calculate moving averages
df['SMA_50'] = df['Close'].rolling(window=50).mean()
df['SMA_200'] = df['Close'].rolling(window=200).mean()

# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, window):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df['Close'], 14)

# Calculate Sharpe Ratio manually
returns = df['Close'].pct_change().dropna()
mean_return = returns.mean()
std_return = returns.std()
sharpe_ratio = mean_return / std_return * np.sqrt(252)  # Annualizing the Sharpe Ratio
print(f'Sharpe Ratio: {sharpe_ratio}')

# Set the style for plots
sns.set(style="whitegrid")

# Plot the stock price and moving averages
plt.figure(figsize=(14, 7))
plt.plot(df['Close'], label='Close Price', color='blue')
plt.plot(df['SMA_50'], label='50-Day SMA', color='red')
plt.plot(df['SMA_200'], label='200-Day SMA', color='green')
plt.title('Stock Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Plot RSI
plt.figure(figsize=(14, 7))
plt.plot(df['RSI'], label='RSI', color='purple')
plt.title('Relative Strength Index (RSI)')
plt.xlabel('Date')
plt.ylabel('RSI')
plt.legend()
plt.show()
