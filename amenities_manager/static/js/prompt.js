function msgReservationExists() {
	openModal("#modal_reservationExists");
	
}

function msgSignedOut(){
	openModal("#modal_notif_signedOut");
}

function openModal(id){
	$(id).openModal({
		dismissible: false
	});
}