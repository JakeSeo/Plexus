var SelectedDates = [];
			var PendingReserveOnDate = [];
			var PendingReserveOnDateCount = [];
			var SelectedTrips = [];
			var tempPendingReserveOnDate = [];
			var tempPendingReserveOnDateCount = [];
			var tempSelectedTrips = [];
			var summaries = [];
			var currentDate;
			
			$(document).on("click", "#okRepeat", function() {
				okRepeat();
			});
			
			function reserve() {
				if(SelectedTrips.length > 0) {
					$.post("AdvancedReserveServlet", { selectedTrips: SelectedTrips}, function(data) {
						window.location.replace(data);
					});
				} else {
					alert("Select a trip first!");
				}
			}
			
			function formatDate(date) {
				var newDate = new Date(date);
				var day = newDate.getDate();
				var month = newDate.getMonth() + 1;
				var year = newDate.getFullYear();
				
				if(month < 10) {
					return "0" + month + "/" + day + "/" + year;
				}
				
				return month + "/" + day + "/" + year;
			}
			
			function transferMainToTemp(tripId, tripDate){
				var elemIndex = SelectedTrips.indexOf(parseInt(tripId));
				if(elemIndex > -1){
					tempSelectedTrips.push(tripId);
					SelectedTrips.splice(elemIndex, 1);
					if(tempPendingReserveOnDate[new Date(tripDate)]==null){
						tempPendingReserveOnDate[new Date(tripDate)]=new Date(tripDate);
					}
					if(tempPendingReserveOnDateCount[tripDate]==null){
						tempPendingReserveOnDateCount[tripDate]=1;
					}else{
						tempPendingReserveOnDateCount[tripDate]=tempPendingReserveOnDateCount[tripDate]+1;
					}
					delete PendingReserveOnDate[new Date(tripDate)];
					delete PendingReserveOnDateCount[new Date(tripDate)];
					
				}
			}
		
			function formatDateTime(timeVal){
				var newDate = new Date(timeVal);
				var h = newDate.getHours();
				var min = padValue(newDate.getMinutes());
				var ampm = "AM";
			
				var hCheck = parseInt(h);
				if(hCheck>=12){
					ampm = "PM";
					h = hCheck - 12;
				}
				else if(hCheck===0){
					h = "12";
				}
				h = padValue(h);
				
				return h+":"+min+" "+ampm;
			}
			
			function padValue(value){
				return (value < 10) ? "0" + value:value;
			}
			
			
			function updateSummary() {
				var currDay = currentDate.getDate();
				var currMonth = currentDate.getMonth();
				var currYear = currentDate.getFullYear();
				
				for(var i = 0; i < summaries.length; i++){
					var s = summaries[i];
					var d = summaries[i].dates;
					for(var j = 0; j < d.length; j++) {
						var date = new Date(d[j]);
						var year = date.getFullYear();
						var day = date.getDate();
						var month = date.getMonth();
						if(currDay === day && currMonth === month && currYear === year) {
							$("#summaryWeek").html(s.summaryWeek);
							var daysString = "";
							for(var k = 0; k < s.summaryDays.length; k++) {
								if(k === 0) {
									daysString += s.summaryDays[k];
								} else {
									daysString += "<br>" + s.summaryDays[k];
								}
							}
							$("#summaryDays").html(daysString);
							$("#summaryFrom").html(s.summaryFrom);
							$("#summaryUntil").html(s.summaryUntil);
							$("#summary").css("visibility", "visible");
							return;
						}
					}
				}
				$("#summary").css("visibility", "hidden");
				//document.getElementById("summary").innerHTML = ""; 
			}
      
			function selectTripPossibleRepeat(tripId, tripDate) {
				var elemIndex = tempSelectedTrips.indexOf(tripId);
				if(elemIndex > -1){
					tempSelectedTrips.splice(elemIndex, 1);
					SelectedTrips.splice(elemIndex, 1);
					tempPendingReserveOnDateCount[tripDate]=tempPendingReserveOnDateCount[tripDate]-1;
					PendingReserveOnDateCount[tripDate]=PendingReserveOnDateCount[tripDate]-1;
					if(tempPendingReserveOnDateCount[tripDate]==0){
						delete tempPendingReserveOnDate[new Date(tripDate)];
						delete tempPendingReserveOnDateCount[new Date(tripDate)];
						delete PendingReserveOnDate[new Date(tripDate)];
						delete PendingReserveOnDateCount[new Date(tripDate)];
					}
				} else {
					tempSelectedTrips.push(tripId);
					SelectedTrips.push(tripId);
					if(tempPendingReserveOnDate[new Date(tripDate)]==null){
						tempPendingReserveOnDate[new Date(tripDate)]=new Date(tripDate);
						PendingReserveOnDate[new Date(tripDate)]=new Date(tripDate);
					}
					if(tempPendingReserveOnDateCount[tripDate]==null){
						tempPendingReserveOnDateCount[tripDate]=1;
						PendingReserveOnDateCount[tripDate]=1;
					} else {
						tempPendingReserveOnDateCount[tripDate]=tempPendingReserveOnDateCount[tripDate]+1;
						PendingReserveOnDateCount[tripDate]=PendingReserveOnDateCount[tripDate]+1;
					}
				}
	            $( "#mainDatepicker" ).datepicker("refresh");
			}
			
	      	function loadTrips(date){
	      		alert("loadtrips: "+SelectedTrips.length);
		      	loadTripsGivenRoute(date, 1);
		      	loadTripsGivenRoute(date, 2);
			}
	      	
	      	function loadTripsGivenRoute(date, routeNum){
		      	$.post('AdvancedGetTrips', { dateObj: date, routeNum:routeNum }, function(responseJson){
		      		var mainDiv;
		      		if(routeNum==1){
		      			mainDiv = $('.stc-to-manila');
		      		}else if(routeNum==2){
		      			mainDiv = $('.manila-to-stc');
		      		}
		      		mainDiv.empty();
		      		if(responseJson!=null){
		      			$.each(responseJson, function(key,value){
		      				var divContainer = $("<div></div>");
		      				var input = $("<input></input").addClass("with-gap")
								.attr("type", "checkbox")
								.attr("name", "groupTrip")
								.attr("id", value['tripId'])
								.attr("onclick", "selectTripPossibleRepeat("+value['tripId']+",\""+value['date']+"\")");
		      				if(value['numReservation'] >= value['tempCapacity']) {
			      				divContainer.addClass("col s12 m12 schedule-container closer-slot");
			      				input.attr("disabled", true);
		      				} else {
			      				divContainer.addClass("col s12 m12 schedule-container open-slot");
		      				}
		      				
		      				var elemIndex = SelectedTrips.indexOf(parseInt(value['tripId']));
		              		if(elemIndex > -1){
		              			//alert("WENT TRUE NIGGGROOOOOO");
		              			transferMainToTemp(parseInt(value['tripId']),value['date']);
		              			input.attr("checked", true);
		              		}
		      				
		      				var label = $("<label></label>").addClass("col s12 m12").attr("for", value['tripId']);
		      				var divTripId = $("<div></div>").addClass("col s6 m6");
		      				var spanTripId = $("<span></span>").addClass("trip-info-label");
		      				spanTripId.html(value['id']);
		      				var divDepTime = $("<div></div>").addClass("col s6 m6 valign");
		      				var spanDepTime = $("<span></span>").addClass("trip-info-label");
		      				spanDepTime.html(formatDateTime(value['depTime']));
		      				
		      				spanTripId.appendTo(divTripId);
		      				spanDepTime.appendTo(divDepTime);
		      				divTripId.appendTo(label);
		      				divDepTime.appendTo(label);
		      				input.appendTo(divContainer);
		      				label.appendTo(divContainer);
		      				divContainer.appendTo(mainDiv);
		      			});
		      		}
		      	}); 
			}
	      	
	      	function okRepeat() {
	    		var days = [];
	    		var daysString= "";
	            $.each($("input[type='checkbox'][name='day']:checked"), function(){   
	                days.push($(this).val());
	                daysString += $(this).val() + " "; 
	            });
	            var week = $( "#week option:selected" ).text();
	            var startDate = $( "#datepicker2" ).val();
	            var selectedvar = $("input[type='radio'][name='radioEnd']:checked").val();
	            var endDate;
	            if(selectedvar == '1') {
	            	endDate = $( "#datepicker3" ).val();
	            } else {
	            	endDate = selectedvar;
	            }
	            stString = "";
	            endDate = formatDate(endDate);
	            for(var i = 0; i < SelectedTrips.length; i++) {
	            	stString += SelectedTrips[i] + " ";
	            }
	            
	    		$.post('RepeatReserveServlet', { days: days, week:week, startDate:startDate, endDate:endDate, SelectedTrips:tempSelectedTrips  }, function(responseJson){
	    			if(responseJson!=null){
	    				var trips = responseJson["trips"];
	    				var dates = [];
	    				$.each(trips, function(key,value){
	    					var tripId = parseInt(value['tripId']);
	    					var tripDate = value['date'];
	    				
	    					dates.push(tripDate);
	    					selectTrip(tripId, tripDate);
	    				});
	    				sd = {
	    						dates: dates,
	    						summaryWeek: week,
	    						summaryDays: days,
	    						summaryFrom: startDate,
	    						summaryUntil: endDate
	    				};
	    				summaries.push(sd);
	    				$.post('SummariesServlet', {summaries: JSON.stringify(summaries)});
	    				updateSummary();
	    			}
	    			var selectedDate = currentDate;
	    			
	    			var dd = currentDate.getDate();
	    			var mm = selectedDate.getMonth()+1; //January is 0!

	    	        var yyyy = selectedDate.getFullYear();
	    	        if(dd<10){
	    	            dd='0'+dd
	    	        } 
	    	        if(mm<10){
	    	            mm='0'+mm
	    	        } 
	    	        var selectedDate = mm + "/" + dd + "/" + yyyy;
	    	        var dateIndex = [];
	    			var countIndex = [];
	    	        for(x in PendingReserveOnDateCount) {
	    	        	dateIndex.push(x);
	    	        	alert("repeat pushed to count: "+PendingReserveOnDateCount[x]);
	    				countIndex.push(PendingReserveOnDateCount[x]);
	    		    }
	    	        $.post('PendingReserveOnDateCountServlet', { pendingReserveOnDateCount: countIndex, pendingReserveOnDateDate:dateIndex});
	    	        $.post('SelectedTripsServlet', { SelectedTrips: SelectedTrips, dateIndex: dateIndex});
	    	        $( "#mainDatepicker" ).datepicker("refresh");
	    	        //loadTrips(selectedDate);
	    	         
	    		});
	    	}
	      	
	      	function selectTrip(tripId, tripDate){
	    		var elemIndex = SelectedTrips.indexOf(tripId);
	    		
	    		if(elemIndex == -1){
	    			SelectedTrips.push(tripId);
	    			if(PendingReserveOnDate[new Date(tripDate)]==null){
	    				PendingReserveOnDate[new Date(tripDate)]=new Date(tripDate);
	    			}
	    			if(PendingReserveOnDateCount[tripDate]==null){
	    				PendingReserveOnDateCount[tripDate]=1;
	    			}else{
	    				PendingReserveOnDateCount[tripDate]=PendingReserveOnDateCount[tripDate]+1;
	    			}
	    		}
	    	}
	      	
            $(function() {
                var dateTomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
                var termEnd = new Date(2016,8,1);

                $("#mainDatepicker").datepicker({
                	language: 'en',
                	minDate: dateTomorrow, 
                	maxDate: termEnd,
                	onRenderCell: function (date, cellType) {
                		var currentDate = date.getDate();
                		var Highlight = SelectedDates[date];
        	            var Hightlight2 = PendingReserveOnDate[date];
        	            if(Hightlight2){
        	            	return {
                    			html: currentDate + '<span class="dp-note"></span>'
                    		}
        	            } else if (Highlight) {
        	            	return {
                    			html: currentDate + '<span class="dp-note"></span>'
                    		}
        	            } else {
        	                return;
        	            }
                		
                		
                	},
        	        onSelect: function(dateText, inst) {
        	        	alert("ONSELECT!!!!");
        	        	currentDate = new Date(dateText);
        	        	for(x in tempPendingReserveOnDate) {
        	        		//alert("onselect-PROD:" +tempPendingReserveOnDate[x]);
        	        		PendingReserveOnDate[tempPendingReserveOnDate[x]] = tempPendingReserveOnDate[x];
        		        }
        	        	
        	        	for(x in tempPendingReserveOnDateCount) {
        	        		//alert("PRODC: "+PendingReserveOnDateCount.length);
        	        		PendingReserveOnDateCount[x] = tempPendingReserveOnDateCount[x];
        		        }
        	        	for(x in PendingReserveOnDateCount) {
        	        		//alert("LEGIT PRODC: "+PendingReserveOnDateCount[x]);
        		        }
        	        	
        	        	for(x in tempSelectedTrips) {
        	        		//alert("ST: "+SelectedTrips.length);
        	        		SelectedTrips.push(tempSelectedTrips[x]);
        		        }
        	        	//alert("I am lit again x3 "+PendingReserveOnDate.length+" "+SelectedTrips.length);
        	        	var dateIndex = [];
						var countIndex = [];
        	        	for(x in PendingReserveOnDateCount) {
        	        		dateIndex.push(x);
        	        		//alert("pushed to count: "+PendingReserveOnDateCount[x]);
        	        		countIndex.push(PendingReserveOnDateCount[x]);
        		        }
        	        	if(SelectedTrips.length>0 && dateIndex.length>0){
        	        		//alert("STORED SHIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIT@@@@@@@"+SelectedTrips+" "+PendingReserveOnDateCount);
        	        	$.post('PendingReserveOnDateCountServlet', { pendingReserveOnDateCount: countIndex, pendingReserveOnDateDate:dateIndex});
        	        	$.post('SelectedTripsServlet', { SelectedTrips: SelectedTrips, dateIndex: dateIndex});
        	        	}
        	        	tempPendingReserveOnDate = [];
        	        	tempPendingReserveOnDateCount = [];
        	        	tempSelectedTrips = [];
        	        	//alert("DATETEXT: "+dateText);
        	            loadTrips(dateText);
        	            updateSummary();
        	            $( "#mainDatepicker" ).datepicker("refresh");
        	            alert("COMES AROUND");
        	        }
            	});
            });
            
            
            $(function() {
                var dateTomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
                var termEnd = new Date(2016,8,1);
                $( "#start-datepicker" ).datepicker({
                	language: 'en',
                	minDate: dateTomorrow, 
                	maxDate: termEnd
                });
            });
            
           
            
            
            $(document).ready(function() {
            	
            	$.getJSON("SelectedTripsServlet", function (data){ 
           		 SelectedTrips=[]; 
           		 PendingReserveOnDate=[]; 
           		if(data[0]!=null && data[1]!=null){
           			//Transfer to temp the selected trip for current selected date for loadtrips
	            		SelectedTrips=data[0].map(Number);  //We get both data1 and data2 from the array
	            		//alert("EXPOSEEE: "+SelectedTrips);
	            		for(x in data[1]){
	            			//alert("PROD!: "+data[1][x]+" fr:"+new Date(data[1][x]));
	            			PendingReserveOnDate[new Date(data[1][x])] = new Date(data[1][x]);
	            		}
	            		initializeSite();
           		}else{
           			initializeSite();
           		}
           		
           		});
           	    //alert("I am lit again "+PendingReserveOnDate.length+" "+SelectedTrips.length);
           	$.get('PendingReserveOnDateCountServlet', function(responseJson){
           		PendingReserveOnDateCount = [];
           		if(responseJson!=null){
           			$.each(responseJson, function(key,value){
           				//alert("GET PRODC ELEM: "+value['count']);
           				PendingReserveOnDateCount[new Date(value['date'])] = value['count'];
           			});
           		}
           	});
           	
            	
            	
            	$.get('HighlightDates', function(responseJson){
            		if(responseJson!=null){
            			$.each(responseJson, function(key,value){
            				SelectedDates[new Date(value['tripDate'])] = new Date(value['tripDate']);
            			});
            		}else{
            		}
            	}); 
            	
            	$.get('SummariesServlet', function(responseJson) {
            		if(responseJson!=null){
            			$.each(responseJson, function(key,value){
            				summaries.push(value);
            			});
            		}else{
            		}
            	});
            	
				//alert("tempPRD:"+tempPendingReserveOnDate.length+" tempPRDC:"+tempPendingReserveOnDateCount.length+" tempST:"+tempSelectedTrips.length);
            	//alert("I AM LIT "+PendingReserveOnDate.length+" "+SelectedTrips.length);
        		$("#mainDatepicker" ).datepicker("refresh");
                $('.modal-trigger').leanModal();
                $('select').material_select();
            });
            
            function initializeSite(){
            	var dateTomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
                var day = dateTomorrow.getDate();
                var month = dateTomorrow.getMonth() + 1;
                var year = dateTomorrow.getFullYear();

                $('#mainDatepicker').data('datepicker').selectDate(dateTomorrow);
                //alert("READY DATETEXT: "+month + "/" + day + "/" + year+" st:"+SelectedTrips.length);
                //loadTrips(month + "/" + day + "/" + year);
				updateSummary();
            }
            
            $('.datepicker-mat').pickadate({
                selectMonths: true, // Creates a dropdown to control month
                selectYears: 15, // Creates a dropdown of 15 years to control year
            });
          
            $(".button-collapse").sideNav();