import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons


# Function to fetch data and plot line graphs for prices and returns
def fetch_data():
    # Get the current date
    today = datetime.datetime.now().date()

    # Calculate the start date for weekly, monthly, and yearly intervals
    start_weekly = today - datetime.timedelta(weeks=52)
    start_monthly = today - datetime.timedelta(days=30)
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

    # Create a dictionary to store the visibility status of each line
    line_visibility = {company: True for company in tickers}

    # Plot the prices and returns for each company
    lines = []
    for company in tickers:
        line_prices, = axs[0].plot(prices[company], label=company, alpha=0.7, visible=line_visibility[company])
        line_returns, = axs[1].plot(returns[company], label=company, alpha=0.7, visible=line_visibility[company])
        line_both, = axs[2].plot(prices[company], label=company, alpha=0.7, visible=line_visibility[company])
        axs[2].plot(returns[company], label=f'{company} Returns', linestyle='--', alpha=0.7,
                    visible=line_visibility[company])
        lines.append((line_prices, line_returns, line_both))

    # Set titles and legends for each subplot
    axs[0].set_title('Prices')
    axs[1].set_title('Returns')
    axs[2].set_title('Prices and Returns')
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()

    # Adjust spacing between subplots
    plt.tight_layout()

    # Create checkboxes for toggling line visibility
    checkboxes_ax = plt.axes([0.91, 0.35, 0.08, 0.3])
    checkboxes = CheckButtons(checkboxes_ax, tickers, [line_visibility[company] for company in tickers])

    # Function to handle checkbox toggling
    def toggle_lines(label):
        line_visibility[label] = not line_visibility[label]
        for line in lines:
            if line[0].get_label() == label:
                line[0].set_visible(line_visibility[label])
                line[1].set_visible(line_visibility[label])
                line[2].set_visible(line_visibility[label])
        plt.draw()

    # Connect the checkbox toggling function to the CheckButtons
    checkboxes.on_clicked(toggle_lines)

    # Show the plot
    plt.show()

    # Fetch the data for all S&P 500 companies
    sp500_data = fetch_sp500_data()

    # Check if stock data was fetched successfully
    if not sp500_data.empty:
        # Calculate the percentage change for the last 6 months
        six_month_returns = sp500_data.pct_change(periods=26).iloc[-1]

        # Sort the percentage changes in descending order to get the top performers (last 6 months)
        top_performers = six_month_returns.sort_values(ascending=False).head(5)

        # Sort the percentage changes in ascending order to get the lowest performers (last 6 months)
        lowest_performers = six_month_returns.sort_values(ascending=True).head(5)

        # Print the top performing stocks (last 6 months)
        print("Top Performing Stocks (Last 6 Months):")
        print(top_performers)

        # Print the lowest performing stocks (last 6 months)
        print("\nLowest Performing Stocks (Last 6 Months):")
        print(lowest_performers)

        # Calculate the percentage change for the last month
        one_month_returns = sp500_data.pct_change(periods=4).iloc[-1]

        # Sort the percentage changes in descending order to get the top performers (last month)
        top_performers_monthly = one_month_returns.sort_values(ascending=False).head(5)

        # Sort the percentage changes in ascending order to get the lowest performers (last month)
        lowest_performers_monthly = one_month_returns.sort_values(ascending=True).head(5)

        # Print the top performing stocks (last month)
        print("\nTop Performing Stocks (Last Month):")
        print(top_performers_monthly)

        # Print the lowest performing stocks (last month)
        print("\nLowest Performing Stocks (Last Month):")
        print(lowest_performers_monthly)


# Function to fetch stock data for S&P 500 companies
def fetch_sp500_data():
    # Get the list of S&P 500 tickers
    sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()

    # Create an empty DataFrame to store the stock prices
    prices_df = pd.DataFrame()

    # Fetch the data for each company using yfinance
    for ticker in sp500_tickers:
        try:
            data = yf.download(ticker, start=datetime.datetime.now() - datetime.timedelta(days=6 * 30),
                               end=datetime.datetime.now())
            prices_df[ticker] = data['Adj Close']
        except Exception as e:
            print(f'Error fetching data for {ticker}: {str(e)}')

    # Drop any columns with missing values
    prices_df.dropna(axis=1, inplace=True)

    return prices_df


# Call the fetch_data() function to fetch data and display the line graphs with the GUI
fetch_data()
