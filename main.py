import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

# Function to fetch data and plot all three charts
def fetch_data():
    # Get the current date
    today = datetime.datetime.now().date()

    # Calculate the start date for weekly, monthly, and yearly intervals
    start_weekly = today - datetime.timedelta(weeks=52)
    start_monthly = today - datetime.timedelta(days=365)
    start_yearly = today - datetime.timedelta(days=365 * 10)

    # Fetch the data using yfinance
    try:
        sp500 = yf.download('^GSPC', start=start_weekly, end=today, interval='1wk')
    except Exception as e:
        print('An error occurred:', str(e))
        return

    # Calculate daily returns
    sp500['daily_return'] = sp500['Close'].pct_change()

    # Drop NaN values
    sp500.dropna(inplace=True)

    # Create subplots for multiple charts
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    # Plot the weekly chart
    axs[0].plot(sp500['Close'])
    axs[0].set_title('Weekly')

    # Fetch the data using yfinance for monthly and yearly intervals
    try:
        sp500_monthly = yf.download('^GSPC', start=start_monthly, end=today, interval='1mo')
        sp500_yearly = yf.download('^GSPC', start=start_yearly, end=today, interval='1mo')
    except Exception as e:
        print('An error occurred:', str(e))
        return

    # Plot the monthly chart
    axs[1].plot(sp500_monthly['Close'])
    axs[1].set_title('Monthly')

    # Plot the yearly chart
    axs[2].plot(sp500_yearly['Close'])
    axs[2].set_title('Yearly')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    plt.show()

# Call the fetch_data() function to fetch data and display the graph
fetch_data()
