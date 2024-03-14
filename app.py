from flask import Flask, render_template, request, jsonify
from utilities import lookup, display_random
import sqlite3
app = Flask(__name__)

database = "stocks.db"

@app.route('/')
def home():
    raw_data = display_random()
    data = [{'name': stock.split(': ')[0], 'price': stock.split(': ')[1]} for stock in raw_data]
    return render_template('home.html', data=data)

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
    cursor.execute('INSERT INTO stock_purchase (symbol, quantity, bought_price, total) VALUES (?, ?, ?, ?)',
                   (symbol, quantity, bought_price, total))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Recorded"})

@app.route('/owned')
def owned():
    raw_data = display_random()
    data = [{'name': stock.split(': ')[0], 'price': stock.split(': ')[1]} for stock in raw_data]
    return render_template('stockowned.html', data=data)
    return render_template('stockowned.html')



if __name__ == '__main__':
    app.run(debug=True)
