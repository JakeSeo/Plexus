function onSignIn(googleUser) {
	

	
	  gapi.auth2.getAuthInstance({
	      client_id: '1035312031605-s9lh4kq3vre7768ffc3h4t11jmodempt.apps.googleusercontent.com'
	  });
	  
	  var profile = googleUser.getBasicProfile();
	  var id_token = googleUser.getAuthResponse().id_token;
	  var email = profile.getEmail();
	  var imgUrl = profile.getImageUrl();
	  var flag = false;
	  
//	  window.alert("TO MNL ID: " + <%=request.getParameter("toMNLid")%> );
	  
//	  var toMNLid = <%=request.getParameter("toMNLid")%>;
//	  var toSTCid = <%=request.getParameter("toSTCid")%>;
//	  var toMNLdropoff = <%= request.getParameter("toMNLdropoff")%>;
//	  var toSTCdropoff = <%=request.getParameter("toSTCdropoff" %>; 
	  
	  
	  

	  
      if(email.indexOf("@dlsu.edu.ph") != -1 || email.indexOf("@delasalle.ph") != -1){
			  $.ajax({
					 type:'POST',	
//					 data:{email: email,
//						   imgUrl: imgUrl,
//						   toMNLid:toMNLid,
//						   toSTCid:toSTCid,
//						   toMNLdropoff:toMNLdropoff,
//						   toSTCdropoff:toSTCdropoff
//						   },
//					 data:{email: email,
//						   imgUrl: imgUrl
//						   },
					 url:'AuthenticationServlet',
					 success: function(response){
					
						 	if(response == "error"){
						 		 openModal("#modal1");
						 	}else{
//						 		alert("response: " + response);
						 		$(location).attr('href', response);
						 	}
						 


		             }
						 
				  });

		  
		 	  
	  }else{
		  alert("Only @dlsu.edu.ph and @delasalle.ph email accounts can be used.");
		  signOut();
	  }
		  



}

function triggerLoginButton(){
	$(".abcRioButtonContentWrapper").click();
}

function openModal(id){
	$(id).openModal({
		dismissible: false
	});
}


	




        		  





	



