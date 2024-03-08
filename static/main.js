$(document).ready(function(){
    $('#search_stock').on('submit', function(e){ //The button where submit is pressed
        e.preventDefault(); // Prevent the default form submission
        $.ajax({
            url: '/search',
            type: 'post',
            dataType: 'json',
            data: $(this).serialize(), // Serialize the form data .//Think of this as okay I want to connect this script to the backend
                                        //the url i want to connect to is /search, type is post and datatype is json, we then serialise this form
                                        //The serialisation is act of connection to the backend
            success: function(response) { //Upon successful response from the backend it is now connected as backened sends data upon retieving from form
                var total = response.total
                var resultHtml = `
                    <div class="search-result">
                        <p>Symbol: ${response.searched_symbol}</p>
                        <input type="number" id="quantity" name="quantity" min="1" value="1">
                        <button id="buy-btn" onclick="buyStock()">Buy</button>
                        <p>Total: $<span id="total">${total}</span></p>
                    </div>    
                `;
        
                $('#search-results').html(resultHtml); //The div with class search-result will render resultHtml

                $('#quantity').on('input', function(){ //Increment something when to quantity increase, id will have #, then datatype
                    var quantity = $(this).val(); //The quantity will take value from the id of data type input
                    $('#total').text((quantity * total).toFixed(2)); //the text of id=total will equal to quantity multiply total 
                });
            }
        });
    });
});

function buyStock() {
    alert(`executing`);
}