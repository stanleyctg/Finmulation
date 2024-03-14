import sqlite3
d = []
# Connect to the SQLite database
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

cursor.execute('SELECT quantity, total FROM stock_purchase WHERE symbol = ?', ("AAPL",))
row = list(cursor.fetchone())

print(row)

# Close the connection
conn.close()
