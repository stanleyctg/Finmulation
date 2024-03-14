import requests #Library to make HTTP request to the finance API
import csv  #API return stock data in CSV format
import uuid #uuid generates unique identifiers
import pytz #pytz provides time zone definitions for all time zones
import datetime 
import random
from urllib.parse import quote_plus #Ensure the stock symbol is properly formatted inclusion in URL




symbol = "AAPL" #Stocks are typically uppercase
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

response = requests.get(url, cookies={"session": str(uuid.uuid4())}, headers={"User-Agent": "python-requests", "Accept": "*/*"})
response.raise_for_status()

# CSV header: Date,Open,High,Low,Close,Adj Close,Volume
quotes = list(csv.DictReader(response.content.decode("utf-8").splitlines()))
quotes.reverse()
prices = []
dates = []
print(quotes)

for quote in quotes:
    dates.append(quote["Date"])
    prices.append(round(float(quote['Adj Close']),2))

print(dates)

# price = round(float(quotes[1]["Adj Close"]), 2)
# print({
#     "name": symbol,
#     "price": price,
#     "symbol": symbol
# })

print(prices)
