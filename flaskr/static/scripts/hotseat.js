
 			//function is called when adding and removing players
			//it's called with a trigger (add or remove) and the player's name
			// DOM is updated dynamically

				//outside of the function above, we want to dynamically check for provide_players_list
				//every time the user lands on the page. this is done on window load
				//this avoids the issue of restarting a game with an existing list but not showing it
				var audio = new Audio('https://www.soundjay.com/button/beep-07.wav');
				var end_audio = new Audio('https://www.soundjay.com/transportation/car-honk-2.wav');
				var game_data

				function play_audio() {
					audio.play()
				}

				function loop_audio() {
					audio.loop = true
					audio.play()
				}

				function stop_audio() {
					audio.loop = false
					end_audio.play()
					audio = new Audio('https://www.soundjay.com/button/beep-07.wav');
				}

				function next_prompt(){
					game_data.splice(0, 1);
					$("#hotseat_prompt").text(game_data[0])
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
									game_data = data.results
									$("#loading_spinner").hide()
									$("#hotseat_prompt").show()
									next_prompt()
									$("#next_button").show()
									// set interval at start of game - beeps every 2 seconds
									var beeper = setInterval(function(){ play_audio(); }, 1000);
									// on a 30 second delay, clear the interval playing at 2 seconds, activate another interval to beep every second
									// this second interval also has a nested clear, on a 20 second timer. Together, this means
									// the 2 seconds runs for 30 seconds and the 1 second beep runs for the next 20 and times out
									setTimeout(function(){  clearInterval(beeper); var faster_beeper = setInterval(function(){ play_audio(); 	setTimeout(function(){ clearInterval(faster_beeper);}, 20000); }, 500); }, 30000);
									// at 50 seconds, the audio begins to loop, causing a very fast beep
									setTimeout(function(){  loop_audio()}, 50000);
									// at 60 seconds, the game ends and prompts are replaced with game over/play again
									setTimeout(function(){  stop_audio(); $("#hotseat_prompt").text("Game over!"); $("#next_button").hide(); $("#start_button").show() }, 60000);
									}
								}
						});
					}
