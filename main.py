import requests
import matplotlib.pyplot as plt

API_KEY = '2J9QRI7DIE1H8YFD'  # Replace with your Alpha Vantage API key


def fetch_stock_data():
    symbol = 'SPY'  # Ticker symbol for S&P 500 ETF
    endpoint = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'

    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise exception for non-2xx HTTP status codes
        data = response.json()

        return data

    except requests.exceptions.RequestException as e:
        print("Error occurred during API request:", e)

    except ValueError as e:
        print("Error occurred while parsing API response:", e)

    return None


def create_chart(data):
    if 'Global Quote' in data:
        global_quote = data['Global Quote']
        current_price = global_quote['05. price']
        previous_close = global_quote['08. previous close']

        labels = ['Previous Close', 'Current Price']
        values = [previous_close, current_price]

        plt.bar(labels, values)
        plt.ylabel('Price')
        plt.title('S&P 500 Stock Data')
        plt.show()

    else:
        print("Error: Missing required data in API response")
        print("API response:", data)


if __name__ == '__main__':
    stock_data = fetch_stock_data()

    if stock_data is not None:
        create_chart(stock_data)
