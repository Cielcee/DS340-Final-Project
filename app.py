"""Streamlit.py

Created in Sublime Text 4.

# Interface Evaluations

In this Python file, we're going to do what we planned for week four: **integrating Streamlit**. Since we have all of the hard work done now—data collection, few-shot prompting, game design—it is time to make the user interface (UI) aesthetically pleasing. This entails:

* Reusing the vast majority of code from week three, given a few major tweaks
* Setting up environments using Windows PowerShell or Bash on Mac and Linux systems
* Typing commands in the command line interface (CLI) to run or debug the game

Here are some things to note before proceeding. 
First: You *can* play the game without Streamlit. Just download the `GameEngine_P2.ipynb` file, swap in your own API key, and run the notebook in Google Colab or an IDE that supports it. It won't look nor feel as good, but it's still feasible.
Second: Google Colab does not natively support Streamlit. It is best practice to not hardcode API keys, try jank tunneling, and run awkward `!pip installs` (among other things). This is why you'll create your own local environment using a CLI.
Third: Be mindful of file directories and CLI sessions. If you close your CLI window, you may have to re-run `pip install streamlit google-genai` and `$env:GEMINI_API_KEY = "your_api_key"` again. You may need to `cd` to the folder containing this file as well.
Fourth: To get started, (1) download this file, (2) open a CLI, (3) run the two commands in the previous note, (4) `cd` to the file's parent folder, (5) then run `streamlit run app.py.` To exit, run `ctrl + c` in the CLI. You're good to go!  
Fifth: For more information on Streamlit, check out their website at https://streamlit.io/.   

Also, we changed the model from Gemini 3 Flash Preview to Gemini 2.5 Flash because it ran into less 503 ServerErrors. Feel free to update the model as you wish.
"""

## Add the dependencies
import streamlit as st
import os
import re
import time
from google import genai
from google.genai import types

## Fetch the API key from the environment, not from Google Colab
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

## Define the evaluator logic using our few-shot-prompted LLM from our week two notebook
evaluator_instruction = (
	"You are a professional comedy writer. Evaluate whether the text is funny or not based on this binary rubric:\n"
	"0 (not funny) if there's no comedic intent, missing a punchline, feels forced, too niche, or unoriginal.\n"
	"1 (funny) if it's unpredictable yet clever, witty and unique, intuitive in its wordplay, or isn't overty offensive.\n"
	"Please be lenient and make it easy for responses to obtain a 1. Assume that delivery, timing, and commitment are all in the user's favor.\n"
	"First, write one brief sentence explaining your reasoning. Then, on a new line, output the final score in this exact format: 'Score: [0/1]'."
)

few_shot_examples = [
	# Hard-coded three examples of class 0 & reasons for their classification
	types.Content(role = 'user', parts = [types.Part.from_text(text = "Text: I used to date Hispanic guys, but now I prefer consensual.")]),
	types.Content(role = 'model', parts = [types.Part.from_text(text = "Reasoning: This is a racist rape joke mocking Hispanic men, making it both overly crude and insensitive. \nScore: 0")]),
	types.Content(role = 'user', parts = [types.Part.from_text(text = "Text: You can get a lot of power out of one inch.")]),
	types.Content(role = 'model', parts = [types.Part.from_text(text = "Reasoning: This is low and almost too easy of a joke to make, so it's unoriginal and not funny. \nScore: 0")]),
	types.Content(role = 'user', parts = [types.Part.from_text(text = "Text: No one notices the Taylor oil spill because it's a disaster taking place over a long period of time, like Derrick Rose's career.")]),
	types.Content(role = 'model', parts = [types.Part.from_text(text = "Reasoning: This comes off as antagonistic since it throws shade at a person, Derrick Rose (whom many consider to be a great but flawed NBA player), and is too unpopular of an opinion, thus not constituting a good joke. \nScore: 0")]),

	# Hard-coded three examples of class 1 & reasons for their classification
	types.Content(role = 'user', parts = [types.Part.from_text(text = "Text: Please, don't call me sir. Call me ma'am.")]),
	types.Content(role = 'model', parts = [types.Part.from_text(text = "Reasoning: This is funny because it is witty and self-deprecating, given that the user is indeed a man. \nScore: 1")]),
	types.Content(role = 'user', parts = [types.Part.from_text(text = "Text: Hey, I am Conan O'Brien and I'm honored to be the last human host of the Academy Awards. Yes! Yeah! Next year, it's going to be a Waymo in a tux.")]),
	types.Content(role = 'model', parts = [types.Part.from_text(text = "Reasoning: This is very funny as it's clever and uses observational comedy to comment on the advent of AI in self-driving cars, like Waymo, whilst keeping it wholesome. \nScore: 1")]),
	types.Content(role = 'user', parts = [types.Part.from_text(text = "Text: How did us teaching Diana to drive turn into I'm a male prostitute, you're going to put me out, and you're going to come back in an hour, and you want your trap full?")]),
	types.Content(role = 'model', parts = [types.Part.from_text(text = "Reasoning: This is funny because, in spite of its unorthodox format (as it doesn't read like a classic joke or pun), it calls out the absurdity of the situation in a unique and unpredictable way. \nScore: 1")])
]

def get_humor_score(player_text):
	'''
	This is, essentially, our flagship LLM in a nutshell.
	It takes the user's input, grades it based on our rubric, and determines whether it's funny (1) or not (0) with ~70%+ accuracy. 
	'''
	turn_input = types.Content(role = 'user', parts = [types.Part.from_text(text = f"Text: {player_text}")])
	response = client.models.generate_content(
		model = "gemini-2.5-flash",
		contents = few_shot_examples + [turn_input],
		config = types.GenerateContentConfig(
			system_instruction = evaluator_instruction,
			temperature = 0
		)
	)
	match = re.search(r'Score:\s*([0-1])', response.text)
	return int(match.group(1)) if match else 0

## Define the game master's instructions
INSTRUCTION = (
	"You are the (dungeon) master for an interactive text-based game in the style of 'Choice of Games.'\n"
	"Your job is to take a basic outline of a skit and expand it into an immersive RPG scene using the following pointers:\n"
	"1. Narrate in the second person (e.g. 'You pull up to...' or 'Your heart races.')\n"
	"2. Write one to two paragraphs totalling no more than half a dozen sentences. Let the complexity of the outline dictate the exact length, just like a real novel\n"
	"3. Ground the player in the scene by describing the setting (i.e. one or more of the five senses—sight, smell, touch, taste, hearing)\n"
	"4. Include at least one piece of dialogue from an NPC interwoven into the scene\n"
	"5. End the final paragraph with an NPC interacting directly to the player. Leave the narrative hanging so that the player must respond."
)

## Define the functions that make up the game engine
def cold_open():
	'''
	A function that gives the user instructions on how the game works. 
	'''
	prompt = "Write a very short cold open explaining that this is a text-based comedy role-playing game, where the user is a college exchange student who should try to be as funny as possible in their responses to each scenario. End with the phrase, 'Live from BU, it's The Terrier Jukebox!'"
	response = client.models.generate_content(
		model = "gemini-2.5-flash",
		contents = prompt,
		config = types.GenerateContentConfig(
			temperature = 0.5
		)
	)
	return response.text

def skitzo(segment_text):
	'''
	A function that calls the LLM to expand upon our pre-written skits.
	'''
	prompt = f"Here's the outline to expand upon: {segment_text}"
	response = client.models.generate_content(
		model = "gemini-2.5-flash",
		contents = prompt,
		config = types.GenerateContentConfig(
			system_instruction = INSTRUCTION,
			temperature = 0.5
		)
	)
	return response.text

def bit(previous_scene, player_action, npc_reaction, bit_text):
	'''
	A function that calls the LLM to expand upon our pre-written bits in context.
	'''
	prompt = (
		f"Earlier in this scene: {previous_scene}\n"
		f"Player said: {player_action}\n"
		f"NPC reacted: {npc_reaction}\n\n"
		f"Now, seamlessly continue the narrative based on this next plot point: {bit_text}"
	)
	response = client.models.generate_content(
		model = "gemini-2.5-flash",
		contents = prompt,
		config = types.GenerateContentConfig(
			system_instruction = INSTRUCTION,
			temperature = 0.5
		)
	)
	return response.text

def npc(scenario, player_text, score, wrap = False):
	'''
	A function that calls the LLM to act as an NPC and react to the player in context.
	'''
	reaction_type = "positive, laughing, and rewarding" if score == 1 else "awkward, offended, or confused"
	WRAP_INSTRUCTION = INSTRUCTION
	if wrap:
		WRAP_INSTRUCTION = INSTRUCTION.replace(
			"5. End the final paragraph with an NPC interacting directly to the player. Leave the narrative hanging so that the player must respond.",
			"5. End the final paragraph with an NPC wrapping up the bit and segment."
		)
	prompt = (
		f"Context: {scenario}\n"
		f"Player's response: {player_text}\n\n"
		f"The player's response was evaluated for humor and got a score of {score}/1. "
		f"Write a short, {reaction_type} response from the NPC reacting to the player."
	)
	response = client.models.generate_content(
		model = "gemini-2.5-flash",
		contents = prompt,
		config = types.GenerateContentConfig(
			system_instruction = INSTRUCTION,
			temperature = 0.5
		)
	)
	return response.text

## Initialize the skits
skits = [
	{
		"Segment": "The user is a college exchange student who wants to sound like a native, so they take a crash course in a foreign language—with special emphasis on learning slang—from an instructor and dialect coach. It is provided that the LLM gives translations for the other tongue in parentheses (akin to subtitles) so that the user may respond in English.",
		"Bit": "The user tries to learn how to say things like their name, greetings, phrases, questions, and body parts."
	},
	{
		"Segment": "The user crashes a club meeting they have never been to before. Is it for freebies? Is it for…um, kicks and giggles? Maybe getting a guy or girl’s number or something?",
		"Bit": "The user sees boxes of Dunkin’ Donuts and Baskin-Robbins on the table, but doesn’t know if they should eat it or not since no one says anything."
	},
	{
		"Segment": "The user takes a part-time job at a convenience store or cafe to make some extra money on the side. And because they want that Employee of the Month (EOM) reward. For a genuine, authentic experience, it sure is a hell of a lot of work.",
		"Bit": "The user is tasked with either welcoming customers and helping them find goods if they are at a convenience store, or being a cashier and receiving calls for orders if they are at a cafe."
	},
	{
		"Segment": "The user surprises their older sibling who is in the middle of a date with their new partner. Like every younger sibling, they proceed to third-wheel for the rest of the day. Poor child…",
		"Bit": "The user accompanies their older sibling and partner to a romantic dinner. At the dinner table, the user decides to do something to break the tension."
	},
	{
		"Segment": "The user is about to finish their exchange program, so they try to cook their homestay dinner as a thank you. Time for a solo visit to the grocery store with a recipe they found on YouTube.",
		"Bit": "The user learns the art of the national cuisine and plays with their food."
	}
]

## Run the game using Streamlit
st.title("The Terrier Jukebox")

## Start the game state on the very first run via Session State (i.e. 'memory' if you will)
if "current_skit" not in st.session_state:
	st.session_state.round = 0
	st.session_state.total_score = 0
	st.session_state.history = []
	st.session_state.phase = 1 # 1: First response (to segment), 2: Second response (to bit), 3: Game over 
	
	with st.spinner("Loading..."):
		intro = cold_open() 
		st.session_state.history.append({"role": "assistant", "content": intro})
		st.session_state.history.append({"role": "assistant", "content": "**SKITZO 1**"}) 
		st.session_state.current_skit = skitzo(skits[0]["Segment"])
		st.session_state.history.append({"role": "assistant", "content": st.session_state.current_skit})

## Show the chat history on every refresh
for msg in st.session_state.history:
	with st.chat_message(msg["role"]):
		st.write(msg["content"])

## Handle the user input & game logic
if player_action := st.chat_input("What do you do/say?", disabled = (st.session_state.phase == 3)): # 'disabled' param disables input when the game's done
	
	st.session_state.history.append({"role": "user", "content": player_action}) # Save the user's input
	
	with st.chat_message("user"): # Show the user's input so the screen doesn't look frozen
		st.write(player_action)
	
	with st.spinner("Thinking..."): # Process the LLM generation before refreshing the screen
		
		try:
			if st.session_state.phase == 1:
				# Grade the user (1st API call)
				score_1 = get_humor_score(player_action)
				st.session_state.total_score += score_1
				
				time.sleep(2) # Pause for 2 seconds to respect rate limits
				
				# Proc NPC reaction (2nd API call)
				reaction_1 = npc(st.session_state.current_skit, player_action, score_1)
				st.session_state.history.append({
					"role": "assistant", 
					"content": f"*[Evaluator Score: {score_1}/1]*\n\n{reaction_1}"
				})
				
				time.sleep(2) # ""
				
				# Segway into bit (3rd API call)
				st.session_state.current_bit = bit(
					st.session_state.current_skit, player_action, reaction_1, skits[st.session_state.round]["Bit"]
				)
				st.session_state.history.append({"role": "assistant", "content": st.session_state.current_bit})
				
				# Move to the second half of the round
				st.session_state.phase = 2
				
			elif st.session_state.phase == 2:
				# Grade the user again (1st API call)
				score_2 = get_humor_score(player_action)
				st.session_state.total_score += score_2
				
				time.sleep(2) # ""
				
				# Proc NPC reaction again (2nd API call)
				reaction_2 = npc(st.session_state.current_bit, player_action, score_2, wrap = True)
				st.session_state.history.append({
					"role": "assistant", 
					"content": f"*[Evaluator Score: {score_2}/1]*\n\n{reaction_2}"
				})
				
				# Increment the round
				st.session_state.round += 1
				
				time.sleep(2) # ""
				
				# Check for more skits, or if it's gg
				if st.session_state.round < len(skits):
					st.session_state.history.append({"role": "assistant", "content": f"**SKITZO {st.session_state.round + 1}**"})
					
					# Move to the next skit (3rd API call)
					st.session_state.current_skit = skitzo(skits[st.session_state.round]["Segment"])
					st.session_state.history.append({"role": "assistant", "content": st.session_state.current_skit})
					
					# Reset phase for the new round
					st.session_state.phase = 1
				else:
					st.session_state.phase = 3
					total_exchanges = len(skits) * 2
					final_score = st.session_state.total_score
					if final_score >= (total_exchanges * 0.8):
						ending_type = "GOOD ENDING: The student is awarded and life quality improves drastically."
						status = "Success/Hero"
					elif final_score >= (total_exchanges * 0.4):
						ending_type = "NEUTRAL ENDING: The student continues daily life as normal."
						status = "Average/Surviving"
					else:
						ending_type = "BAD ENDING: The student is jailed or expelled from the country."
						status = "Failure/Criminal"
					running_story = "\n".join([msg["content"] for msg in st.session_state.history if msg["role"] == "assistant"])
					final_prompt = f"""
                    You are the narrator of an interactive comedy game about an exchange student.
                    The game is over. Here is the summary of the player's journey:
					{running_story}

                    FINAL RESULT: {ending_type}

                    Write a cinematic, funny closing narration (2-3 paragraphs) that concludes the student's story
                    based on the result above. Reference specific events from the story history to make it feel
                    cohesive.
                    """
					final_narrative_response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=final_prompt,
                        config=types.GenerateContentConfig(temperature=0.7)
                    )
					st.session_state.history.append({"role": "assistant", "content": f"**FINAL STATUS: {status}**"})
					st.session_state.history.append({"role": "assistant", "content": f"**Final Score: {final_score}/{total_exchanges}**"})
					st.session_state.history.append({"role": "assistant", "content": final_narrative_response.text})
				'''
				else:
					# Endgame branching
					st.session_state.phase = 3
					st.session_state.history.append({"role": "assistant", "content": "**Good game!**"})
					
					final_score = st.session_state.total_score
					if final_score == 10:
						signoff = "You were pretty funny! Thanks for playing."
					elif final_score > 5:
						signoff = "You will get funnier. Thanks for playing."
					else:
						signoff = "You made a valiant effort. Thanks for playing."
						
					st.session_state.history.append({
						"role": "assistant", 
						"content": f"**Final Score: {final_score}/10**\n\n{signoff}"
					})
				'''

				


			# Only refresh the page if the API call is successful
			st.rerun()

		except Exception as e:
			st.session_state.history.pop() # Remove the user's last input from memory if the API fails
			st.error("The API hiccuped! Please wait a few seconds and try submitting your response again.") # Display an actually useful error message 