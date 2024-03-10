# Finmulation
Description:
This project involves the use of yahoo finance to retrieve real time prices for stocks, the simulation starts with users having a sum of $10,000 as a default balance. Users can use this balance to buy stocks and sell stocks! There will be a chart that shows balance against time, use as an indication of their performance in beating the market.

Total Overview:
A login system that uses flask sessions to differentiate their respective data.
Homepage where users can search for a specific stock, then it will display the price of the stock along with the quantity and buy button.
An "owned" button in the Navbar that takes user to the page that display all the stocks they have owned, these price per stock bought are compared to the price of the stock currently and provides feedback such as loss or profits or remain. example if I bought an apple stock for $170, and the current price is $175 then it shows I will get a profit of $5 by selling it.

Functionalities:
When a user buys stocks, it should decrease their balance and add it to their purchase history and the stocks owned along with details of the price per stock bought.
When a user press sells, it directs them to stock owned page and increase their balance based on the current price of the stock and remove them from the stocks owned page.
When user checks their performance t returns a page that display a chart of their balance against time weekly, there will also be another line on the same graph that shows the asset plus balance of the user of what they could have if they sold everything.
All these will be linked to the database. 

Database:
User_credentials table- consists of unique usernames, and passwords.
Profile- consists of stocks owned, quantity, bought price, date bought.

Language used: Flask(python), HTML, CSS, Javascript (AJAX, chart.js), SQLite3
 
5 weeks to complete before moving into market predictions.
Weekly agendas:
Week1: Prepare all the pages. Allow user to search for symbols, and display price of each stock with quantity and buy button. (Done)
Week2: Complete buy function and add it to the purchase history and stocks owned page. At this point should start on database.
Week3: Complete sell function and performance chart.
Week4: Complete login system 
Week5: Additional styling
