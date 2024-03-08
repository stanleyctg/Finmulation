$(document).ready(function(){
    $('#search_stock').on('submit', function(e){
        e.preventDefault(); // Prevent the default form submission
        $.ajax({
            url: '/search',
            type: 'post',
            dataType: 'json',
            data: $(this).serialize(), // Serialize the form data
            success: function(response) {
                // Directly use response.total as the unit price
                const unitPrice = response.total; 
                
                // Use the searched_symbol directly for display
                const displayText = response.searched_symbol; 

                const resultHtml = `
                    <div class="search-result">
                        <p>${displayText}</p>
                        <label for="quantity-${response.searched_symbol}">Quantity:</label>
                        <input type="number" id="quantity-${response.searched_symbol}" name="quantity" min="1" value="1">
                        <button type="button" onclick="buyStock('${response.searched_symbol}', ${unitPrice})">Buy</button>
                        <p>Total: $<span id="total-${response.searched_symbol}">${unitPrice}</span></p>
                    </div>
                `;
                $('#search-results').html(resultHtml);

                // Update total when quantity changes
                $(`#quantity-${response.searched_symbol}`).on('input', function() {
                    const newQuantity = $(this).val();
                    const newTotal = newQuantity * unitPrice;
                    $(`#total-${response.searched_symbol}`).text(newTotal.toFixed(2));
                });
            }
        });
    });
});

function buyStock(symbol, price) {
    const quantity = $(`#quantity-${symbol}`).val();
    const total = quantity * price;
    alert(`Buying ${quantity} of ${symbol} for a total of $${total.toFixed(2)}`);
}


