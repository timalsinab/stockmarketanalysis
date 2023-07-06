import pandas as pd
import yfinance as yf
import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Function to fetch data based on the selected interval
def fetch_data(interval):
    # Get the current date
    today = datetime.datetime.now().date()

    # Calculate the start date based on the selected interval
    if interval == 'Weekly':
        start = today - datetime.timedelta(weeks=52)
    elif interval == 'Monthly':
        start = today - datetime.timedelta(weeks=52 * 5)
    elif interval == 'Yearly':
        start = today - datetime.timedelta(weeks=52 * 10)
    else:
        messagebox.showerror('Error', 'Invalid interval selected.')
        return

    # Fetch the data using yfinance
    try:
        sp500 = yf.download('^GSPC', start=start, end=today, interval='1d')
    except Exception as e:
        messagebox.showerror('Error', str(e))
        return

    # Calculate daily returns
    sp500['daily_return'] = sp500['Close'].pct_change()

    # Drop NaN values
    sp500.dropna(inplace=True)

    # Plot the data
    sp500['daily_return'].plot(title='S&P 500 Daily Returns')
    sp500['Close'].plot(title='S&P 500 Price')

    # Show the plot
    plt.show()

# Function to create the GUI
def create_gui():
    # Create the GUI window
    window = tk.Tk()
    window.title('S&P 500 Data')

    # Increase the size of the window
    window.geometry('600x400')

    # Create buttons for different intervals
    btn_weekly = tk.Button(window, text='Weekly', command=lambda: fetch_data('Weekly'))
    btn_weekly.pack()

    btn_monthly = tk.Button(window, text='Monthly', command=lambda: fetch_data('Monthly'))
    btn_monthly.pack()

    btn_yearly = tk.Button(window, text='Yearly', command=lambda: fetch_data('Yearly'))
    btn_yearly.pack()

    # Start the GUI event loop
    window.mainloop()

# Call the create_gui() function to create and run the GUI
create_gui()
