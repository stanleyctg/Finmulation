import sqlite3

# Create a new database if not exist ("stocks.db")
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()
# Create table for stock_purchase that shows what you've bought
# This show the owned stock which is very different from history table
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_purchase(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    bought_price REAL NOT NULL,
    total REAL NOT NULL
)
''')
# Create account_details that holds balance
cursor.execute('''
CREATE TABLE IF NOT EXISTS account_details(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    balance INTEGER NOT NULL
)
''')
# Create purchase history to display what have been bought at what date
cursor.execute('''
CREATE TABLE IF NOT EXISTS purchase_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    bought_price REAL NOT NULL,
    total REAL NOT NULL,
    date DATETIME NOT NULL
)
''')
# Create table for portfolio that holds total_assets and date
cursor.execute('''
CREATE TABLE IF NOT EXISTS portfolio(
    id INTEGER PRIMARY KEY,
    total_assets REAL NOT NULL,
    date DATETIME NOT NULL
)
''')
# Insert account details with a user for now
cursor.execute("""INSERT INTO account_details
                (username, password, balance)
                VALUES (?,?,?)""", ("stanleyctg", 12345, 10000))
conn.commit()
conn.close()
