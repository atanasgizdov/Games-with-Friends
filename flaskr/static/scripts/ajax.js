			//Enter submits the add_player function

			//var input = document.getElementById("player_name");
			//input.addEventListener("keyup", function(event) {
  		//if (event.keyCode === 13) {
   		//	event.preventDefault();
   		//	document.getElementById("add_player").click();
  		//	}
			//});

 			//function is called when adding and removing players
			//it's called with a trigger (add or remove) and the player's name
			// DOM is updated dynamically
			function add_remove_players(trigger, player_name){

				if (trigger == "remove_player")
					player_name = player_name.value
				else

						//trigger = trigger.trim(); // remove any spaces around the text
						player_name = player_name.replace(/\s/g,""); // remove any spaces around the text

						$.ajax({
							url: "add_remove_players", //URL called to Python Flask app
							data: {trigger: trigger, player_name: player_name}, //search values
							dataType: "json",
							success: function(data){
								var res = "";
								var start_button = "";

								//set the text field back to empty so the next player can be entered
								document.getElementById('player_name').value = null
								//re-focus cursor on input
								document.getElementById('player_name').focus()
								// create the html with results
								for(player in data.results){ // JSON result example: {"results": [[516, "0743290119", "Lauren Weisberger", "Chasing Harry Winston"]]} where results are book id, ISBN, Author and Book Title
									res += "<button type=\"button\" class=\"btn btn-info\" value =" + data.results[player]+ " onclick=\"add_remove_players(\'remove_player\', this)\" style=\"border:1px solid; border-color:black\">"+data.results[player]+"</button>";
								} // above logic constructs results with JSON data, as well as contructing a "View" link, via book id, to the book's page

								$("#players_list").html(res); // build each result into the html in a list to the corresnding results element in index.html

								if (data.results.length > 2){
									start_button = "<a href=\"play\" class=\"btn btn-lg btn-secondary\">Start Game</a>"
									$("#start_button").html(start_button);
									}
								else {
									start_button = ""
									$("#start_button").html(start_button);
								}
							}
						});

				}

				//outside of the function above, we want to dynamically check for provide_players_list
				//every time the user lands on the page. this is done on window load
				//this avoids the issue of restarting a game with an existing list but not showing it
				function check_for_players(){
					$.ajax({
						url: "players_list", //URL called to Python Flask app
						data: {}, //search values
						dataType: "json",
						success: function(data){

							console.log(data)
							var res = "";
							var start_button = "";

							if (data.results === undefined || data.results == 0){
								$("#players_list").html("");
							}
							else {
							// create the html with results
							for(player in data.results){ // JSON result example: {"results": [[516, "0743290119", "Lauren Weisberger", "Chasing Harry Winston"]]} where results are book id, ISBN, Author and Book Title
								res += "<button type=\"button\" class=\"btn btn-info\" value =" + data.results[player]+ " onclick=\"add_remove_players(\'remove_player\', this)\" style=\"border:1px solid; border-color:black\">"+data.results[player]+"</button>";
							} // above logic constructs results with JSON data, as well as contructing a "View" link, via book id, to the book's page

							$("#players_list").html(res); // build each result into the html in a list to the corresnding results element in index.html

							if (data.results.length > 2){
								start_button = "<a href=\"play\" class=\"btn btn-lg btn-secondary\">Start Game</a>"
								$("#start_button").html(start_button);
								}
							else {
								start_button = ""
								$("#start_button").html(start_button);
								}
							}
						}
					});
				}
