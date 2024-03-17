import sqlite3

conn = sqlite3.connect("stocks.db")

cursor = conn.cursor()

cursor.execute("SELECT quantity, total, id, bought_price FROM stock_purchase WHERE symbol = ?", ("MSFT",))
row = cursor.fetchone()

conn.commit()
conn.close()

print(row)