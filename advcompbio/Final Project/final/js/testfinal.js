// this function executes our search via an AJAX call
function runSearch( term ) {
    // hide and clear the previous results, if any
    $('#results').hide();
    $('tbody').empty();
    
    // transforms all the form parameters into a string we can send to the server
    var frmStr = $('#search_term').serialize();
    alert('ajax call');
    $.ajax({
	    url: './testfinal.cgi',
	 	dataType: 'json',
	 	data: frmStr,
		success: function(data, textStatus, jqXHR) {
		alert("pre process");
		processJSON(data);
		alert("success");
	    },
		error: function(jqXHR, textStatus, errorThrown){
		alert("Failed to perform BLAST search! textStatus: (" + textStatus +
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
    alert(next_row_num);
    // iterate over each match and add a row to the result table for each
    $.each( data.matches, function(i, item) {
	    var this_row_id = 'result_row_' + next_row_num++;	    
        // create a row and append it to the body of the table
	    /*
	      $href->{'database'}=$db[$i];
	      $href->{'accession'}=$acc[$i];
	      $href->{'description'}=$desc[$i];
	      $href->{'score'}=$score[$i];
	      $href->{'evalue'}=$evalue[$i];
	     */
	    $('<tr/>', { "id" : this_row_id } ).appendTo('tbody');	    
	    alert('table');
	    $('<td/>', { "text" : item.database } ).appendTo('#' + this_row_id);	    
	    alert('database');
	    $('<td/>', { "text" : item.accession } ).appendTo('#' + this_row_id);	    
	    alert('accession');
	    $('<td/>', { "text" : item.description } ).appendTo('#' + this_row_id); 
	    alert('description');
	    $('<td/>', { "text" : item.score } ).appendTo('#' + this_row_id);
	    alert('score');
	    $('<td/>', { "text" : item.evalue } ).appendTo('#' + this_row_id);
	    alert('evalue');
	});
    
    // now show the result section that was previously hidden
    $('#results').show();

}
// run our javascript once the page is ready
$(document).ready( function() {
	// define what should happen when a user clicks submit on our search form
	$('#submit').click( function() {
		runSearch();
		return false;  // prevents 'normal' form submission
	    });
    });
