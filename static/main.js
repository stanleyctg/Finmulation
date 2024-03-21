$(document).ready(function(){
    var balanceText = $('#balance').text(); 
    var balanceAmount = parseInt(balanceText.replace(/[^0-9]/g, ''), 10);
    $('#search_stock').on('submit', function(e){
        e.preventDefault(); // Prevent the default form submission
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

                $(`#quantity-${symbol}`).on('input', function(){
                    var quantity = $(this).val();
                    $(`#total-${symbol}`).text((quantity * pricePerStock).toFixed(2));
                });

                // Remove any existing click handlers from previous searches and add special id to specific symbol searched
                $(document).off('click', '#buy-btn-' + symbol).on('click', '#buy-btn-' + symbol, function() {
                    var quantity = $(`#quantity-${symbol}`).val();
                    var totalCost = (pricePerStock * quantity).toFixed(2);
                    buyStock(symbol, quantity, totalCost, pricePerStock, balanceAmount);
                });
                var x = response.past_data[1]
                var y = response.past_data[0]
                drawSymbolChart(symbol, x, y); // Pass symbol as argument
            }
        });
    });
});

function drawSymbolChart(symbol, x, y) { // Accept symbol as parameter
    var ctx = document.getElementById('chart-container').getContext('2d');
    var xValues = x;
    var yValues = y

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


function buyStock(symbol, quantity, totalCost, pricePerStock, balanceAmount) {
    //Connect these data into flask to add into database
    var balanceT = document.getElementById("balance");
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
            alert(response.new_balance);
            balanceT.innerHTML = "Balance: $" + response.new_balance;
        },
        error: function() {
            alert("Error");
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Listen for input on any quantity input
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
    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('[id^="sell-btn-"]').forEach(button => {
            button.addEventListener('click', function() {
                var balanceT = document.getElementById("balance");
                var symbol = this.id.split('-')[2];
                var quantity = document.querySelector(`#quantity-${symbol}`).value;
                var sellRate = parseFloat(document.querySelector(`#sellRate-${symbol}`).innerText.replace('$', ''));
                var totalSale = (quantity * sellRate).toFixed(2);
    
                alert(`Selling ${quantity} of ${symbol} for a total of $${totalSale} at $${sellRate} per unit.`);
            
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
    
    
    document.addEventListener("DOMContentLoaded", function() {
        // Generate random dataset    
        const ctx = document.getElementById('profile-chart-container').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [2,3,5],
                datasets: [{
                    label: "Portfolio Chart",
                    data: [1,2,3],
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "x-values",
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
                            text: "y-values",
                            font: {
                                lineHeight: 1.2,
                                weight: 'bold'
                            }
                        }
                    }
                }
            }
        });
    });
    


// function setupChart() { 
//     var months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
//     var countList = [2,3,4,5,6,7,8,9,1,2,3,4];

//     }
//     const ctx = document.getElementById('homeChart').getContext('2d');
//     const myChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
//             datasets: [{
//                 label: "Workouts per Month",
//                 data: countList,
//                 backgroundColor: 'rgba(255, 99, 132, 0.2)',
//                 borderColor: 'rgba(255, 99, 132, 1)',
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: false,
//                     ticks: {
//                         stepSize: 1,
//                         precision: 0
//                     }
//                 }
//             }
//         }
//     });
// document.addEventListener('DOMContentLoaded', function() {
//     setupChart(window.chartDates);
// });