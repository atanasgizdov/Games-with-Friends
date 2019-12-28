
 			//function is called when adding and removing players
			//it's called with a trigger (add or remove) and the player's name
			// DOM is updated dynamically

				//outside of the function above, we want to dynamically check for provide_players_list
				//every time the user lands on the page. this is done on window load
				//this avoids the issue of restarting a game with an existing list but not showing it
				var audio = new Audio('https://www.soundjay.com/button/beep-07.wav');

				function play_audio() {
					audio.play()
				}

					function start_hotseat(){
						//show loading_spinner
						$("#loading_spinner").show()
						//hide buttons
						$("#hotseat_prompt").hide()
						$("#start_button").hide()

						$.ajax({
							url: "get_hotseat_prompts", //URL called to Python Flask app
							data: {}, //search values
							dataType: "json",
							success: function(data){

								console.log(data)

								if (data.results === undefined || data.results == 0){
									$("#loading_spinner").hide()
									$("#hotseat_prompt").text("The DB didn't find any prompts - please try again")
									$("#hotseat_prompt").show()
								}
								else {
								// create the html with results
									$("#loading_spinner").hide()
									$("#hotseat_prompt").text(data.results[0])
									$("#hotseat_prompt").show()
									$("#next_button").show()
									setInterval(function(){ play_audio(); }, 2000);
									}
								}
						});
					}
