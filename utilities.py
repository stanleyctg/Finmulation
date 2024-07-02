import yfinance as yf


# Method to search information on a stock
def lookup(symbol):
    symbol = symbol.upper()
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        price = round(data['Close'].iloc[-1], 2)
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except Exception as e:
        print("An error occurred:", e)
        return None


# Fetch historical data of stock to illustrate chart
def lookup_chart(symbol):
    symbol = symbol.upper()
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1wk")
        dates = data.index.strftime('%Y-%m-%d').tolist()
        prices = data['Close'].tolist()
        return [prices, dates]
    except Exception as e:
        print("An error occurred:", e)
        return None
