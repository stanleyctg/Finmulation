import yfinance as yf

def lookup(symbol):
    symbol = symbol.upper()
    try:
        # Fetch data for the symbol
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        
        # Get the latest adjusted close price
        price = round(data['Close'].iloc[-1], 2)
        
        return {
            "name": symbol,
            "price": price,
            "symbol": symbol
        }
    except Exception as e:
        print("An error occurred:", e)
        return None

def lookup_chart(symbol):
    symbol = symbol.upper()
    try:
        # Fetch historical data for the symbol
        stock = yf.Ticker(symbol)
        data = stock.history(period="1wk")
        
        # Extract dates and adjusted close prices
        dates = data.index.strftime('%Y-%m-%d').tolist()
        prices = data['Close'].tolist()
        
        return [prices, dates]
    except Exception as e:
        print("An error occurred:", e)
        return None