Stock Trading Simulation Project
Description
This project is a stock trading simulation platform that retrieves real-time stock prices using Yahoo Finance. Users start with a default balance of $10,000, which they can use to buy and sell stocks. A performance chart shows the user's balance over time, indicating their success in beating the market.

Features Overview
Login System: Utilizes Flask sessions to manage user data.
Homepage: Users can search for specific stocks and view their current prices. They can also specify quantities and buy stocks.
Owned Stocks Page: Accessible from the Navbar, this page displays all stocks owned by the user. It compares the purchase price to the current price, showing profit or loss.
Buy Function: Decreases the user's balance and adds the purchased stocks to their portfolio.
Sell Function: Increases the user's balance based on the current stock price and removes sold stocks from the portfolio.
Performance Chart: Displays the user's balance over time on a weekly basis, including a comparison line showing potential assets if all stocks were sold.
Functionalities
Buying Stocks: When a user buys stocks, their balance decreases, and the purchase is recorded in their history and portfolio with details such as price per stock and quantity.
Selling Stocks: Users can sell stocks from the owned stocks page, increasing their balance based on the current stock price and updating their portfolio accordingly.
Performance Monitoring: Users can view a performance chart that shows their balance over time, including a comparison of potential assets if all stocks were sold.
Database Structure
User_Credentials Table: Stores unique usernames and passwords.
Profile Table: Stores information on stocks owned, including quantity, purchase price, and purchase date.
Technologies Used
Backend: Flask (Python)
Frontend: HTML, CSS, JavaScript (AJAX, Chart.js)
Database: SQLite3
Future Development
Market Prediction Model: Implement a predictive model for stock trends to assist users in making informed decisions.
