import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

# Function to fetch data and plot line graphs for prices and returns
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

    # Extract the adjusted closing prices
    prices = data['Adj Close']

    # Calculate the weekly, monthly, and yearly returns
    returns = prices.pct_change().dropna()

    # Create subplots for prices and returns
    fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

    # Plot the prices and returns for each company
    for company in tickers:
        axs[0].plot(prices[company], label=company, alpha=0.7)
        axs[1].plot(returns[company], label=company, alpha=0.7)
        axs[2].plot(prices[company], label=company, alpha=0.7)
        axs[2].plot(returns[company], label=f'{company} Returns', linestyle='--', alpha=0.7)

    # Set titles and legends for each subplot
    axs[0].set_title('Prices')
    axs[1].set_title('Returns')
    axs[2].set_title('Prices and Returns')
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()

# Call the fetch_data() function to fetch data and display the line graphs
fetch_data()
