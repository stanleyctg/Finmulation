import sqlite3

conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_purchase(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

cursor.execute('''
CREATE TABLE IF NOT EXISTS purchase_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    bought_price REAL NOT NULL,
    total REAL NOT NULL
)
''')

cursor.execute("""INSERT INTO account_details
                (username, password, balance)
                VALUES (?,?,?)""", ("stanleyctg", 12345, 10000))
conn.commit()
conn.close()
