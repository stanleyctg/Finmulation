from flask import Flask, render_template, request, jsonify, g
from utilities import lookup, lookup_chart
import sqlite3

app = Flask(__name__)
database = "stocks.db"


@app.context_processor
def inject_user():
    db = g._database = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM
                    account_details
                    WHERE username = ?""", ('stanleyctg',))
    account_details = cursor.fetchone()
    return {'account': account_details}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def search():
    symbol = request.form['symbol']
    data = lookup(symbol)
    past_data = lookup_chart(symbol)
    total = data["price"]
    data_final = data["name"] + " : " + "$" + str(data["price"])
    return jsonify(searched_symbol=data_final,
                   total=total, past_data=past_data)


@app.route('/sell', methods=['POST'])
def sell_stock():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    total = float(request.form['total'])
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""SELECT balance
                    FROM account_details
                    WHERE username = ?""", ("stanleyctg",))
    balance_row = cursor.fetchone()
    new_balance = round(balance_row[0] + total, 2)
    cursor.execute("""UPDATE account_details
                    SET balance = ?
                    WHERE username = ?""", (new_balance, "stanleyctg"))
    cursor.execute("""SELECT quantity, total,
                    id, bought_price
                    FROM stock_purchase
                    WHERE symbol = ?""", (symbol,))
    row = cursor.fetchone()
    if row:
        new_quantity = row[0] - quantity
        if new_quantity == 0:
            cursor.execute("""DELETE FROM stock_purchase
                            WHERE symbol = ?""", (symbol,))
        else:
            cursor.execute("""UPDATE stock_purchase
                            SET quantity = ?
                            WHERE symbol = ?""", (new_quantity, symbol))
            new_total = round(row[1] - (quantity * row[-1]), 2)
            cursor.execute("""UPDATE stock_purchase
                            SET total = ?
                            WHERE symbol = ?""", (new_total, symbol))
    conn.commit()
    conn.close()
    return jsonify({"new_balance": new_balance})


@app.route('/buy', methods=['POST'])
def buy_stock():
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    bought_price = float(request.form['boughtPrice'])
    total = float(request.form["total"])
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO purchase_history
                    (symbol, quantity, bought_price, total)
                    VALUES (?, ?, ?, ?) """,
                     (symbol, quantity, bought_price, total))
    cursor.execute("""SELECT balance
                   FROM account_details
                   WHERE username = ?""", ("stanleyctg",))
    balance_row = cursor.fetchone()
    if balance_row[0] < total:
        new_balance = balance_row[0]
        message = "Not enough funds"
    else:
        message = "Recorded"
        new_balance = round(balance_row[0] - total, 2)
        cursor.execute("""UPDATE account_details
                       SET balance = ? WHERE username = ?""",
                       (new_balance, "stanleyctg"))
        cursor.execute("""SELECT quantity, total
                       FROM stock_purchase
                       WHERE symbol = ?""", (symbol,))
        row = cursor.fetchone()
        if row:
            # Symbol exists, update the row
            new_quantity = row[0] + quantity
            new_total = row[1] + total
            new_total = round(new_total, 2)
            cursor.execute("""UPDATE stock_purchase
                           SET quantity = ?, total = ?
                           WHERE symbol = ?""",
                           (new_quantity, new_total, symbol))
        else:
            cursor.execute("""INSERT INTO stock_purchase
                           (symbol, quantity, bought_price, total)
                           VALUES (?, ?, ?, ?)""",
                           (symbol, quantity, bought_price, total))
    conn.commit()
    conn.close()
    return jsonify({"success": True,
                    "message": message,
                    "new_balance": new_balance})


@app.route('/owned')
def owned():
    data = []
    priceUnit = []
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stock_purchase")
    rows = cursor.fetchall()
    for row in rows:
        data.append(list(row))
        priceUnit.append(list(row)[1])
    for i in range(len(priceUnit)):
        symbol_dict = (lookup(priceUnit[i]))
        priceUnit[i] = symbol_dict["price"]

    i, j = 0, 0
    while i < len(data):
        data[i].append(priceUnit[j])
        i += 1
        j += 1
    for stock in data:
        profit_loss_per_unit = stock[5] - stock[3]
        total_profit_loss = profit_loss_per_unit * stock[2]
        if profit_loss_per_unit > 0:
            unit_message = f"Profit: ${profit_loss_per_unit:.2f}/unit"
            total_message = f"Total Profit: ${total_profit_loss:.2f}"
        else:
            unit_message = f"Loss: ${abs(profit_loss_per_unit):.2f}/unit"
            total_message = f"Total Loss: ${abs(total_profit_loss):.2f}"
        # Append the message to the sublist
        stock.append(unit_message)
        stock.append(total_message)

    return render_template('stockowned.html', data=data, priceUnit=priceUnit)

@app.route('/profile')
def profile():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    data = []

    cursor.execute("SELECT * FROM purchase_history")
    rows = cursor.fetchall()
    for row in rows:
        data.append(list(row))

    data.reverse()
    return render_template("profile.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
