$(document).ready(function(){
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
                    buyStock(symbol, quantity, totalCost, pricePerStock);
                });
            }
        });
    });
});

function buyStock(symbol, quantity, totalCost, pricePerStock) {
    alert(`Buying ${quantity} stocks of ${symbol} for a total of $${totalCost} where each stock costs $${pricePerStock}`);
}
