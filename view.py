import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("stocks.db")
cursor = conn.cursor()

# Now, query the table to see all rows
query = "SELECT * FROM stock_purchase"
cursor.execute(query)

# Fetch and print all rows of data
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
