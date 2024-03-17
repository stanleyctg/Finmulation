import sqlite3

conn = sqlite3.connect("stocks.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_purchase (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    bought_price REAL NOT NULL,
    total REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS account_details(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    balance INTEGER NOT NULL
)
''')

conn.commit()
conn.close()