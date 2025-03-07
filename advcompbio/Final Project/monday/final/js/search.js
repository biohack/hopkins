/*
http://jqueryui.com/autocomplete/#remote-jsonp
https://github.com/devbridge/jQuery-Autocomplete/blob/master/scripts/demo.js
 */

// this function executes our search via an AJAX call
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#gene_search').serialize();

    $.ajax({
        url: './search_product.cgi',
	dataType: 'json',
        data: frmStr,
        success: function(data, textStatus, jqXHR) {
            processJSON(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert("Failed to perform gene search! textStatus: (" + textStatus +
                  ") and errorThrown: (" + errorThrown + ")");
	    }
	});
}

// this processes a passed JSON structure representing gene matches and draws it
//  to the result table
function processJSON( data ) {

    // set the span that lists the match count
    $('#match_count').text( data.match_count );
    // this will be used to keep track of row identifiers
    var next_row_num = 1;
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
	    var this_row_id = 'result_row_' + next_row_num++;	    
        // create a row and append it to the body of the table
	    $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');	    
	    // add the locus column
	    $('<td/>', { "text" : item.locus } ).appendTo('#' + this_row_id);	    
	    // add the product column
	    $('<td/>', { "text" : item.product } ).appendTo('#' + this_row_id);	    
	});
    
    // now show the result section that was previously hidden
    $('#results').show();

}
//this function gives suggestions for input when user begins to type via an AJAX call
function autocomplete(){
    $( "#search_term" ).autocomplete({
            source: function( request, response ) {
                //var name = request.term;
                //              var paramStr = name;
                var paramStr = $('#gene_search').serialize();
                var maxRows = 5;
                $.ajax({
                        url: './search_product.cgi',
                            dataType: 'json',
                            data: paramStr,
                            maxRows: 5,
                            success: function( data ) {
                            response( $.map( data.matches, function( item ) {
                                        return {
                                            label: item.product,
						value: item.product
                                                }
                                    }));
                        }
                    });
            },
                minLength: 3,
                open: function() {
                $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
            },
                close: function() {
                $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
            }
        });
}


// run our javascript once the page is ready
$(document).ready( function() {
	// add the autocomplete to the search text box
	$(function(){
		autocomplete();
	    });

	// define what should happen when a user clicks submit on our search form
	$('#submit').click( function() {
		runSearch();
		return false;  // prevents 'normal' form submission
	    });
    });
