from flask import Flask, render_template, request, jsonify
from utilities import lookup, display_random
import sqlite3
app = Flask(__name__)

database = "stocks.db"

@app.route('/')
def home():
    # raw_data = display_random()
    # data = [{'name': stock.split(': ')[0], 'price': stock.split(': ')[1]} for stock in raw_data]
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    symbol = request.form['symbol']
    data = lookup(symbol)
    total = data["price"]
    data_final = data["name"] + " : " + "$" + str(data["price"])
    return jsonify(searched_symbol=data_final, total=total)

@app.route('/buy', methods=['POST'])
def buy_stock():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    bought_price = float(request.form['boughtPrice'])
    total = float(request.form["total"])
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT quantity, total FROM stock_purchase WHERE symbol = ?', (symbol,))
    row = cursor.fetchone()

    if row:
        # Symbol exists, update the row
        new_quantity = row[0] + quantity
        new_total = row[1] + total
        new_total = round(new_total, 2)
        cursor.execute('UPDATE stock_purchase SET quantity = ?, total = ? WHERE symbol = ?',
                       (new_quantity, new_total, symbol))
    else:
        cursor.execute('INSERT INTO stock_purchase (symbol, quantity, bought_price, total) VALUES (?, ?, ?, ?)',
                    (symbol, quantity, bought_price, total))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Recorded"})

@app.route('/owned')
def owned():
    data = []
    priceUnit = []
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    query = "SELECT * FROM stock_purchase"
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        data.append(list(row))
        priceUnit.append(list(row)[1])
    for i in range(len(priceUnit)):
        symbol_dict = (lookup(priceUnit[i]))
        priceUnit[i] = symbol_dict["price"]

    i = 0
    j = 0

    while i < len(data):
        data[i].append(priceUnit[j])
        i += 1
        j += 1
    
    print(data)
    return render_template('stockowned.html', data=data, priceUnit=priceUnit)



if __name__ == '__main__':
    app.run(debug=True)
