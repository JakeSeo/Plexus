var title = document.title;	

if((title == "Book" || title == "Book - Confirm")){
	
	$( "#navBook" ).addClass( "active" );
}

if((title == "Manage")){
	
	$( "#navManage" ).addClass( "active" );
}


if((title == "Trips")){
	
	$( "#navTrips" ).addClass( "active" );
}

$( window ).resize(function() {
	  $( "#profile" ).hide();
	  $( "#sidenav-overlay").click(); 
	});