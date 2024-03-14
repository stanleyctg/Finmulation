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

conn.commit()
conn.close()