$(document).ready(function(){
    $('#search_stock').on('submit', function(e){
        e.preventDefault(); // Prevent the default form submission
        $.ajax({
            url: '/search',
            type: 'post',
            dataType: 'json',
            data: $(this).serialize(), // Serialize the form data
            success: function(response) {
                var total = response.total
                var resultHtml = `
                    <div class="search-result">
                        <p>Symbol: ${response.searched_symbol}</p>
                        <input type="number" id="quantity" name="quantity" min="1" value="1">
                        <button id="buy-btn">Buy</button>
                        <p>Total: $<span id="total">${total}</span></p>
                    </div>    
                `;
        
                $('#search-results').html(resultHtml);

                $('#quantity').on('input', function(){
                    var quantity = $(this).val();
                    $('#total').text((quantity * total).toFixed(2));
                });
            }
        });
    });
});

function buyStock(symbol) {
    const quantity = $(`#quantity-${symbol}`).val();
    alert(`Buying ${quantity} of ${symbol}`);
}
