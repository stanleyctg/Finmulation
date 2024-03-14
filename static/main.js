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
                `;
        
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
            }
        });
    });
});

function buyStock(symbol, quantity, totalCost, pricePerStock, balanceAmount) {
    //Connect these data into flask to add into database
    balanceAmount = balanceAmount - totalCost;
    balanceAmount.toFixed(2);
    var balanceT = document.getElementById("balance");
    balanceT.innerHTML = "Balance: $" + balanceAmount;
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
        },
        error: function() {
            alert("Error");
        }
    });
}
