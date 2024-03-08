from flask import Flask, render_template, request, jsonify
from utilities import lookup
app = Flask(__name__)

data = lookup("AAPL")
print(data)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    symbol = request.form['symbol']
    data = lookup(symbol)
    total = data["price"]
    data_final = data["name"] + " : " + "$" + str(data["price"])
    return jsonify(searched_symbol=data_final, total=total)

if __name__ == '__main__':
    app.run(debug=True)
