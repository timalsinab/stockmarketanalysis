import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import numpy as np

# Function to fetch data and plot bar plots for each company
def fetch_data():
    # Get the current date
    today = datetime.datetime.now().date()

    # Calculate the start date for weekly, monthly, and yearly intervals
    start_weekly = today - datetime.timedelta(weeks=52)
    start_monthly = today - datetime.timedelta(days=365)
    start_yearly = today - datetime.timedelta(days=365 * 10)

    # Define the ticker symbols for the companies
    tickers = ['MSFT', 'AMZN', 'AAPL', '^GSPC']

    # Fetch the data using yfinance
    try:
        data = yf.download(tickers, start=start_weekly, end=today, interval='1wk')
    except Exception as e:
        print('An error occurred:', str(e))
        return

    # Calculate the weekly, monthly, and yearly returns
    weekly_returns = data['Adj Close'].pct_change().dropna()
    monthly_returns = data['Adj Close'].resample('M').ffill().pct_change().dropna()
    yearly_returns = data['Adj Close'].resample('Y').ffill().pct_change().dropna()

    # Define the x-axis labels for each interval
    weekly_labels = weekly_returns.index.strftime('%Y-%m-%d')
    monthly_labels = monthly_returns.index.strftime('%Y-%m')
    yearly_labels = yearly_returns.index.strftime('%Y')

    # Create subplots for multiple bar plots
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # Plot the weekly bar plot
    axs[0].bar(np.arange(len(weekly_returns)), weekly_returns['MSFT'], label='Microsoft')
    axs[0].bar(np.arange(len(weekly_returns)), weekly_returns['AMZN'], label='Amazon')
    axs[0].bar(np.arange(len(weekly_returns)), weekly_returns['AAPL'], label='Apple')
    axs[0].bar(np.arange(len(weekly_returns)), weekly_returns['^GSPC'], label='S&P 500')
    axs[0].set_xticks(np.arange(len(weekly_returns)))
    axs[0].set_xticklabels(weekly_labels, rotation=90)
    axs[0].set_title('Weekly Returns')
    axs[0].legend()

    # Plot the monthly bar plot
    axs[1].bar(np.arange(len(monthly_returns)), monthly_returns['MSFT'], label='Microsoft')
    axs[1].bar(np.arange(len(monthly_returns)), monthly_returns['AMZN'], label='Amazon')
    axs[1].bar(np.arange(len(monthly_returns)), monthly_returns['AAPL'], label='Apple')
    axs[1].bar(np.arange(len(monthly_returns)), monthly_returns['^GSPC'], label='S&P 500')
    axs[1].set_xticks(np.arange(len(monthly_returns)))
    axs[1].set_xticklabels(monthly_labels, rotation=90)
    axs[1].set_title('Monthly Returns')
    axs[1].legend()

    # Plot the yearly bar plot
    axs[2].bar(np.arange(len(yearly_returns)), yearly_returns['MSFT'], label='Microsoft')
    axs[2].bar(np.arange(len(yearly_returns)),yearly_returns['AMZN'], label='Amazon')
    axs[2].bar(np.arange(len(yearly_returns)), yearly_returns['AAPL'], label='Apple')
    axs[2].bar(np.arange(len(yearly_returns)), yearly_returns['^GSPC'], label='S&P 500')
    axs[2].set_xticks(np.arange(len(yearly_returns)))
    axs[2].set_xticklabels(yearly_labels, rotation=90)
    axs[2].set_title('Yearly Returns')
    axs[2].legend()

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()

# Call the fetch_data() function to fetch data and display the bar plots
fetch_data()
