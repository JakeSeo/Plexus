//	$('.dropdown-button').dropdown({
//	    inDuration: 300,
//	    outDuration: 225,
//	    constrain_width: true, // Does not change width of dropdown to that of the activator
//	    hover: false, // Activate on hover
//	    gutter: 0, // Spacing from edge
//	    belowOrigin: false, // Displays dropdown below the button
//	    alignment: 'left' // Displays dropdown with edge aligned to the left of button
//	  }
//	);


function signOut() {
		console.log("@ signout");
	   var auth2 = gapi.auth2.getAuthInstance({
		      client_id: '1035312031605-s9lh4kq3vre7768ffc3h4t11jmodempt.apps.googleusercontent.com'
		  });
	   
	    auth2.signOut().then(function () {
	    	
	    });

    $.ajax({
			 type:'GET',
			 url:'AuthenticationServlet',
			 success: function(response){
//				 msgSignedOut();
//				 
//				 setTimeout(function(){
//					 $(location).attr('href', response);		 	
//					}, 1000 * 1.5);
				 $(location).attr('href', response);		
			 }
    });
    
    return true;
   
}

function signOut2() {
   var auth2 = gapi.auth2.getAuthInstance({
	      client_id: '1035312031605-s9lh4kq3vre7768ffc3h4t11jmodempt.apps.googleusercontent.com'
	  });
   
    auth2.signOut().then(function () {
    	
    });
    
    document.cookie = "error=login_error";
    $(location).attr('href', "login.jsp");
    

    return true;
}

