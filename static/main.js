// This function display the prices of stock when searched
$(document).ready(function(){
    // Obtain the text and the amount
    var balanceText = $('#balance').text(); 
    var balanceAmount = parseInt(balanceText.replace(/[^0-9]/g, ''), 10);
    $('#search_stock').on('submit', function(e){
        e.preventDefault(); 
        // Using ajax to display connect to the backend at '/search'
        $.ajax({
            url: '/search',
            type: 'post',
            dataType: 'json',
            data: $(this).serialize(),
            success: function(response) {
                var symbol = response.searched_symbol.split(":")[0].trim();
                var pricePerStock = response.total; 

                var resultHtml = `
                    <div class="search-result">
                        <p>Symbol: ${symbol}</p>
                        <input type="number" id="quantity-${symbol}" name="quantity" min="1" value="1">
                        <button id="buy-btn-${symbol}">Buy</button>
                        <p>Total: $<span id="total-${symbol}">${pricePerStock}</span></p>
                    </div>    
                    <div class="row chartContainer">
                        <canvas id="chart-container"></canvas>
                    </div>`
        
                $('#search-results').html(resultHtml);

                // Enable change of the total as user select more quantities
                $(`#quantity-${symbol}`).on('input', function(){
                    var quantity = $(this).val();
                    $(`#total-${symbol}`).text((quantity * pricePerStock).toFixed(2));
                });

                $(document).off('click', '#buy-btn-' + symbol).on('click', '#buy-btn-' + symbol, function() {
                    var quantity = $(`#quantity-${symbol}`).val();
                    var totalCost = (pricePerStock * quantity).toFixed(2);
                    buyStock(symbol, quantity, totalCost, pricePerStock);
                });
                // Retrieving the history data of stock place them in x and y variable to draw chart
                var x = response.past_data[1]
                var y = response.past_data[0]
                drawSymbolChart(symbol, x, y);
            }
        });
    });
});


// Using the parameters and draw the chart that shows price history 
function drawSymbolChart(symbol, x, y) { 
    var ctx = document.getElementById('chart-container').getContext('2d');
    var xValues = x;
    var yValues = y

    // Draw the chart with appropriate labels and values
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xValues,
            datasets: [{
                label: `${symbol} Price`,
                data: yValues,
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Date (yyyy/mm/dd)",
                        font: {
                            lineHeight: 1.2,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: "Price ($)",
                        font: {
                            lineHeight: 1.2,
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    });
}


// Sends purchase history to the database
function buyStock(symbol, quantity, totalCost, pricePerStock) {
    var balanceT = document.getElementById("balance");
    // Connect to the '/buy/ route to send data to be accessed
    $.ajax({
        url: '/buy',
        type: 'post',
        data: {
            symbol: symbol,
            quantity: quantity,
            boughtPrice: pricePerStock,
            total: totalCost
        },

        success: function(response){
            alert(response.message);
            balanceT.innerHTML = "Balance: $" + response.new_balance;
        },
        error: function() {
            alert("Error");
        }
    });
}


// This function is at the owned page to handle the change in total when quantity changes
document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('[id^="quantity-"]').forEach(input => {
            input.value  = 1
            input.addEventListener('input', function() {
                var symbol = this.id.split('-')[1];
                var sellRate = parseFloat(document.getElementById(`sellRate-${symbol}`).innerText.replace('$', ''));
                var newTotal = this.value * sellRate;

                document.getElementById(`total-${symbol}`).innerText = newTotal.toFixed(2);

            });
        });
    });


// This function handles the sell function in the owned page
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('[id^="sell-btn-"]').forEach(button => {
        button.addEventListener('click', function() {
            // Get the necessary data which send to backend
            var balanceT = document.getElementById("balance");
            var symbol = this.id.split('-')[2];
            var quantity = document.querySelector(`#quantity-${symbol}`).value;
            var sellRate = parseFloat(document.querySelector(`#sellRate-${symbol}`).innerText.replace('$', ''));
            var totalSale = (quantity * sellRate).toFixed(2);
            alert(`Selling ${quantity} of ${symbol} for a total of $${totalSale} at $${sellRate} per unit.`);
            
            // Send the data to '/sell' route
            $.ajax({
                url: '/sell',
                type: 'POST',
                data: {
                    symbol: symbol,
                    quantity: quantity,
                    boughtPrice: sellRate,
                    total: totalSale
                },
                success: function(response){
                    alert(response.new_balance);
                    balanceT.innerHTML = "Balance: $" + response.new_balance;
                    location.reload()
                },
                error: function() {
                    alert("Error sale");
                }
            });    
        });
    });
});


// This function is to draw portfolio chart at profile
document.addEventListener("DOMContentLoaded", function() {
    // Fecth data from backend 
    fetch('/profile/data')
    .then(response => response.json())
    .then(final_portfolio => {
    const ctx = document.getElementById('profile-chart-container').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: final_portfolio[1],
            datasets: [{
                label: "Portfolio Chart",
                data: final_portfolio[0],
                borderColor: 'rgb(75, 192, 192)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            yMin: 10000,
                            yMax: 10000,
                            borderColor: 'lightblue',
                            borderWidth: 4,
                            label: {
                                content: 'default',
                                enabled: false,
                                position: 'start',
                            }
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Date (yyyy-mm-dd)",
                        font: {
                            lineHeight: 1.2,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: "Net balance ($)",
                        font: {
                            lineHeight: 1.2,
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    })
    });
});
