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
        "This line extracts the dictionary object with the key 'Global Quote' from the data dictionary. " \
        "The data dictionary contains the API response data obtained from Alpha Vantage. " \
        "The 'Global Quote' key holds the specific stock quote information for the requested symbol."
        global_quote = data['Global Quote']
        "This line retrieves the value associated with the key '05. price' from the global_quote dictionary. " \
        "The '05. price' key represents the current price of the stock."
        current_price = global_quote['05. price']
        "This line fetches the value associated with the key '08. previous close' from the global_quote dictionary. " \
        "The '08. previous close' key corresponds to the previous closing price of the stock."
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
