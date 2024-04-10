from flask import Flask, render_template, request, jsonify, g
from utilities import lookup, lookup_chart
from datetime import datetime
import sqlite3

app = Flask(__name__)
database = "stocks.db"


# Inject user details into the website system to be accessed
@app.context_processor
def inject_user():
    # Connect to the database and retrieve user account details
    db = g._database = sqlite3.connect(database)
    db.row_factory = sqlite3.Row
    # Get the specific user detail
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM
                    account_details
                    WHERE username = ?""", ('stanleyctg',))
    account_details = cursor.fetchone()
    # Return the detail that accessible from html files
    return {'account': account_details}


# At route '/' return home.html template
@app.route('/')
def home():
    return render_template('home.html')


# At route '/search' search the symbol for its stock price
@app.route('/search', methods=['POST'])
def search():
    # Symbol is retrieved via form
    symbol = request.form['symbol']
    # Get the price using lookup function
    data = lookup(symbol)
    # Get history data
    past_data = lookup_chart(symbol)
    total = data["price"]
    # Format the string
    data_final = data["name"] + " : " + "$" + str(data["price"])
    # Return the values to be used in asynchronous javascript
    return jsonify(searched_symbol=data_final,
                   total=total, past_data=past_data)


# At route '/sell', handles the sell function for stock
@app.route('/sell', methods=['POST'])
def sell_stock():
    # Obtain the necessary data from frontend
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    total = float(request.form['total'])

    # Connect the database to access the balance and update it
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
    # Delete the stock which was sold
    cursor.execute("""SELECT quantity, total,
                    id, bought_price
                    FROM stock_purchase
                    WHERE symbol = ?""", (symbol,))
    row = cursor.fetchone()
    if row:
        # If there is no more quantity simply delete the row
        # else update the quantity
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
    # Return the new balance which will update the html pages
    return jsonify({"new_balance": new_balance})


# At route '/buy', this handles the buy function of stocks
@app.route('/buy', methods=['POST'])
def buy_stock():
    # Get the necessary data from the frontend
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    bought_price = float(request.form['boughtPrice'])
    total = float(request.form["total"])

    # Connect to the database, and insert the data into history
    conn = sqlite3.connect(database)
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO purchase_history
                    (symbol, quantity, bought_price, total, date)
                    VALUES (?, ?, ?, ?, ?) """, (symbol, quantity,
                                                 bought_price, total, date))
    # Alter the balance based on the total cost
    cursor.execute("""SELECT balance
                   FROM account_details
                   WHERE username = ?""", ("stanleyctg",))
    balance_row = cursor.fetchone()
    # If there is not enough funds, pop an error message
    # else continue with buying process
    if balance_row[0] < total:
        new_balance = balance_row[0]
        message = "Not enough funds"
    else:
        message = "Recorded"
        new_balance = round(balance_row[0] - total, 2)
        # Update balance and quantity
        cursor.execute("""UPDATE account_details
                       SET balance = ? WHERE username = ?""",
                       (new_balance, "stanleyctg"))
        cursor.execute("""SELECT quantity, total
                       FROM stock_purchase
                       WHERE symbol = ?""", (symbol,))
        row = cursor.fetchone()
        if row:
            # Symbol exists, update the row
            # Else create a new one
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
    # Return messages
    return jsonify({"success": True,
                    "message": message,
                    "new_balance": new_balance})


# At route '/owned' it handles the owned page
@app.route('/owned')
def owned():
    # Initialise data and priceUnit to empty lists
    data, priceUnit = [], []

    # Connect to the database
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Retrieve data like the symbol, price, unit, total cost, etc
    # Populate the empty lists
    cursor.execute("SELECT * FROM stock_purchase")
    rows = cursor.fetchall()
    for row in rows:
        data.append(list(row))
        priceUnit.append(list(row)[1])
    # Price Unit is seperate list to obtain the latest price of stock
    for i in range(len(priceUnit)):
        symbol_dict = (lookup(priceUnit[i]))
        priceUnit[i] = symbol_dict["price"]

    # Add the actual price to the data
    i, j = 0, 0
    while i < len(data):
        data[i].append(priceUnit[j])
        i += 1
        j += 1
    # Create feedback messages for profit/loss
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
    # Return html page and the data to be sent
    return render_template('stockowned.html', data=data, priceUnit=priceUnit)


# At route '/profile' handles the profile page
@app.route('/profile')
def profile():
    # Portfolio_balances to be global as used to draw charts
    # Initialise required lists and variables
    global portfolio_balances
    history_data, data, priceUnit, portfolio_balances = [], [], [], []
    total = 0

    # Calculate the liquid asset + balance
    # Connect to the database and collect the current balance
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""SELECT balance FROM account_details
                   WHERE username = ?""", ('stanleyctg',))
    balance_available = cursor.fetchone()
    total += balance_available[0]
    # Get the prices of liquid asset
    cursor.execute("SELECT * FROM stock_purchase")
    rows = cursor.fetchall()
    for row in rows:
        data.append(list(row))
        priceUnit.append(list(row)[1])
    for i in range(len(priceUnit)):
        symbol_dict = (lookup(priceUnit[i]))
        priceUnit[i] = symbol_dict["price"]

    j, k = 0, 0
    while j < len(data):
        # Add the total with the liquid assets
        total += data[j][2] * priceUnit[k]
        j += 1
        k += 1
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    # Insert into the table with the total and current date
    cursor.execute("""INSERT INTO portfolio
                   (total_assets, date)
                   VALUES (?, ?)""", (total, date))
    cursor.execute("SELECT * FROM purchase_history")
    rows = cursor.fetchall()
    # Shows purchase history over 10 purchases
    for row in rows[-10:]:
        history_data.append(list(row))
    history_data.reverse()
    conn.commit()

    # Populate portfolio balance with balances and dates
    cursor.execute("SELECT total_assets, date FROM portfolio")
    # Ensure that earlier dates come first by reversing
    assets_row = cursor.fetchall()
    assets_row.reverse()
    # Show 7 latest unique dates
    dates = sorted(list(set([row[1] for row in assets_row])), reverse=True)[:7]
    start = 0
    for row in assets_row:
        for i in range(start, len(dates)):
            if row[1] == dates[i]:
                portfolio_balances.append(row)
                start += 1
    portfolio_balances.reverse()
    conn.close()
    # Return html page with history data to be accessed
    return render_template("profile.html", data=history_data)


# At route '/profile/data/, handles the portfolio data to draw chart
@app.route('/profile/data')
def get_portfolio_balances():
    # Split the final portfolio to 2 elements of total and balance lists
    final_portfolio = [
        [portfolio_balance[0] for portfolio_balance in portfolio_balances],
        [portfolio_balance[1] for portfolio_balance in portfolio_balances]
    ]
    # Return this data to javascript
    return jsonify(final_portfolio)


if __name__ == '__main__':
    app.run(debug=True)
