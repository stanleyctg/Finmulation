import requests #Library to make HTTP request to the finance API
import csv  #API return stock data in CSV format
import uuid #uuid generates unique identifiers
import pytz #pytz provides time zone definitions for all time zones
import datetime 
import random
from urllib.parse import quote_plus #Ensure the stock symbol is properly formatted inclusion in URL

def lookup(symbol):
    """Look up quote for symbol."""

    # Prepare API request, and get the necessary nformation to call api
    symbol = symbol.upper() #Stocks are typically uppercase
    end = datetime.datetime.now(pytz.timezone("US/Eastern")) 
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        quotes.reverse()
        price = round(float(quotes[0]["Adj Close"]), 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None


def lookup_chart(symbol):
    """Look up quote for symbol."""

    # Prepare API request, and get the necessary nformation to call api
    symbol = symbol.upper() #Stocks are typically uppercase
    end = datetime.datetime.now(pytz.timezone("US/Eastern")) 
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    url = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history&includeAdjustedClose=true"
    )

    # Query API
    try:
        response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
        response.raise_for_status()

        # CSV header: Date,Open,High,Low,Close,Adj Close,Volume
        quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
        prices = []
        dates = []

        for quote in quotes:
            dates.append(quote["Date"])
            prices.append(round(float(quote['Adj Close']),2))
        
        data_chart = [prices, dates]
        return data_chart
    
    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None
    

def display_random():
    all_symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB', 'TSLA', 'BRK-A', 'V', 'JPM', 'JNJ', 'XOM', 'BAC', 'WMT', 'PG', 'CVX', 'PFE', 'TMO', 'UNH', 'DIS']
    data = []
    # Randomly select 10 unique stock symbols
    random_symbols = random.sample(all_symbols, 10)

    # Fetch and print the stock data for the selected symbols
    for symbol in random_symbols:
        stock_data = lookup(symbol)
        if stock_data:
            data.append(f"{stock_data['name']}: ${stock_data['price']}")
        else:
            print(f"Data for {symbol} not found.")

    return data

print(lookup_chart("AAPL"))