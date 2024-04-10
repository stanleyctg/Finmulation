import yfinance as yf


# Looks up the price of a symbol
# Takes symbol as a parameter and returns the price
def lookup(symbol):
    # Converts symbol to upper to match the library
    symbol = symbol.upper()
    # Try to get the data else catch the error
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        # Retrieve the close price of the stock
        price = round(data['Close'].iloc[-1], 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except Exception as e:
        print("An error occurred:", e)
        return None


# Looks up prices of the stock over a week period
# Takes symbol as parameter and returns a list of price and dates
def lookup_chart(symbol):
    # Converts symbol to upper to match the library
    symbol = symbol.upper()
    # Try to get data else catch the error
    try:
        stock = yf.Ticker(symbol)
        # Obtain history of the stock over 1 week
        data = stock.history(period="1wk")
        # Obtain the dates
        dates = data.index.strftime('%Y-%m-%d').tolist()
        # Retrieve the close price of stock over the 1 week period
        prices = data['Close'].tolist()
        return [prices, dates]
    except Exception as e:
        print("An error occurred:", e)
        return None
