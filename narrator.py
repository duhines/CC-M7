"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:
	This module implements 3 classes:
	1. Narrator - 
		the entity that maintains the story knowledge such as setting and
		characters and keeps track of other meta data as the narrative 
		progresses
	2. Event - 
		used an an object to store the time and event for a narrative
		event. 
	3. Episode - 
		Structure that uses the narrator to generate a narrative of some
		length.  

Notes:
	* output will be a text script of TV episodes (maybe build this up to
	seasons?)

"""

import random
import knowledge as knows
import character
from random import choice
import os

NUM_CHARACTERS = 10
NUM_LOCATIONS = 5
RATE_LOCATION_CONNECTED = 1
NUM_ACTIONS = 25

NUM_SCRIPTS = 100
RESULTS_PATH = 'results'
RESULTS_NAME = 'script_'

class Narrator:
	"""
	Purpose: control the flow of the story / keep track of story information
	Includes the following methods:
		characters_at
		can_act
		change_location
		init_locations
		init_characters
	"""
	def __init__(self):
		self.knowledge = knows.Knowledge()
		self.locations = self.init_locations()
		self.characters = self.init_characters()
		self.current_location = choice(self.locations['names'])
		self.social_network = character.SocialNetwork(self.characters)
		self.story_over = False

	def characters_at(self, location):
		"""
		Purpose: return a list of characters in a location.
		"""
		characters = []
		for character in self.characters:
			if character.location == location:
				characters.append(character)
		return characters

	def can_act(self, nearby_characters):
		"""
		Purpose: return a sublist of characters than can actually make an
		action. 
		"""
		can_act = nearby_characters.copy()
		for character in nearby_characters:
			if not character.can_act(self.locations, self.characters,
				nearby_characters, self.social_network):
				can_act.remove(character)
			if not character.alive:
				can_act.remove(character)

		return can_act

	def change_location(self):
		"""
		Purpose: change the current_location to a new location.
		"""
		possibilities = self.locations['names'].copy()
		# don't want to switch to the current location
		possibilities.remove(self.current_location)
		# don't want to focus on a location without any characters
		with_characters = possibilities.copy()
		for possibility in possibilities:
			if self.characters_at(possibility) == []:
				with_characters.remove(possibility)
		if len(possibilities) == 0:
			return 'There are no characters left.'
		else:
			new_location = choice(with_characters)
			self.current_location = new_location
			return 'We now shift our attention to {}'.format(self.current_location)

	def init_locations(self, num_locations=NUM_LOCATIONS):
		"""
		Purpose: create a kind of world map where there are locations from the
		knowledge base connected by edges.
		"""
		chosen_locations = []
		for i in range(0, num_locations):
			location = choice(self.knowledge.locations)
			self.knowledge.locations.remove(location)
			chosen_locations.append(location)
		# dictionary to express connections between locations:
		# connections['location'] = [True, True, False, False,...]
		# ->True if there is a connection between the two locations, false
		#   otherwise
		connections = {}
		for location in chosen_locations:
			options = chosen_locations.copy()
			options.remove(location)
			connected = []
			for option in options:
				connected.append(random.random() < RATE_LOCATION_CONNECTED)
			
			connections[location] = connected

		locations = {
			'names': chosen_locations,
			'connections': connections
		}
		return locations


	def init_characters(self, num_characters=NUM_CHARACTERS):
		"""
		Purpose: create some character objects
		"""
		characters = []
		for i in range(0, num_characters):
			# def __init__(self, name, personality, goal, health, location):
			name = choice(self.knowledge.names)
			# don't want multiple characters to have the same name
			self.knowledge.names.remove(name)
			personality = character.Personality()
			goal = None
			health = random.randint(0, 100)
			location = choice(self.locations['names'])
			characters.append(character.Character(name, personality, goal, health, location))
		return characters


class Event:
	"""
	Keep track of the time that an event occured during.  Using a class
	because dot notation is better than dictionaries.
	"""
	def __init__(self, time, action):
		self.time = time
		self.action = action


# TODO: flesh things out so that the same narrator can create multiple episodes
# of narrative (as long as there are still characters left!)
# class Season: 
# 	"""
# 	Purpose: preserve details of characters and setting accross episodes
# 	"""
# 	def __init__(self, characters, setting):
# 		return 


class Episode: 
	"""
	Purpose: generated scripts organized into episodes, multiple 
	episodes can be told by the same narrator (i.e. same characters
	and setting).
	Includes the following methods:
		write_narrative
		write_script
		get_narrative_from_action
		evaluate
		output_script
	"""
	def __init__(self, narrator, num_actions=NUM_ACTIONS):
		self.narrator = narrator
		self.narrative = []
		self.script = []
		self.num_actions = num_actions
		self.time = 0
		self.starting_connections = []
		self.final_connections = []
		self.score = -1

	def write_narrative(self):
		"""
		Purpose: determine the sequences of actions that make up the script.   
		""" 
		narrator = self.narrator
		curr_acts = 0
		events = []
		opener = 'We begin our story in {}.  '.format(narrator.current_location)
		for character in narrator.characters_at(narrator.current_location):
			opener += '{} is here.  '.format(character)
		opener += '\n'
		# this would be used for a string representation of the social
		# structure, but we don't use this
		initial_social_structre = narrator.social_network.for_narrative()
		self.starting_connections = narrator.social_network.for_fitness()
		
		for character in narrator.characters:
			opener += character.tell_personality() + '\n'
		events.append(Event(0, opener))

		while curr_acts < self.num_actions:
			# want to only be focused on locations where there are characters than
			# can do things
			possible_characters = narrator.characters_at(narrator.current_location)
			can_act = narrator.can_act(possible_characters)
			
			if len(can_act) == 0:
				change_narrative_location = narrator.change_location()
				events.append(Event(self.time, change_narrative_location))
				if change_narrative_location == 'There are no characters left.':
					# the story is OVER
					narrator.story_over = True
					break
			else:
				next_actor = choice(can_act)
				act = next_actor.action_maker(narrator.locations, 
					narrator.characters, possible_characters, narrator.social_network)
				events.append(Event(self.time, act))
				curr_acts += 1

			self.time += 1

		self.final_connections = narrator.social_network.for_fitness()
		closer = 'And thus ends the episode.  \n'
		# this would be used for a string representation of the social
		# structure, but we don't use this
		end_social_structre = narrator.social_network.for_narrative()
		events.append(Event(self.time, closer))
		self.narrative = events

	def write_script(self):
		"""
		Purpose: from a list of actions, get the narrative elements from each 
		event.  
		"""
		for event in self.narrative:
			self.script.append(self.get_narrative_from_action(event))


	def get_narrative_from_action(self, event):
		"""
		Purpose: translate a event into a string representing the event. 
		"""
		# TODO: set up way of getting narrative form that's more interesting
		# (BIG TODO)
		return str(event.action.strip())

	def evalutate(self):
		"""
		Purpose: evalutate an episode of the script by summing the change
		in the connection parameters between the characters. 
		"""
		changes = []
		total_theta = 0
		for i in range(0, len(self.starting_connections)):
			for j in range(0, len(self.starting_connections[i])):
				total_theta += abs(self.starting_connections[i][j] -
					self.final_connections[i][j])
		
		self.score = total_theta
		return total_theta

	def output_script(self):
		"""
		Purpose: write the script to the output folder.
		"""
		# list the number of things in results folder, use that number
		# for a unique file name
		num_results = len(os.listdir(RESULTS_PATH))
		file_name = RESULTS_NAME + str(num_results) + '.txt'
		file = open(RESULTS_PATH + '/' + file_name, 'w')
		for event in self.script:
			file.write(event + '\n')


def main():
	narrator = Narrator()
	episodes = []
	bsf = []
	bsf_score = 0
	# generate 100 scripts using this narrator and choose the one with the 
	# highest fitness, which is currently a measure of how dramatically
	# character connection values changed from the start of the episode 
	# to the end.  
	for i in range(0, NUM_SCRIPTS):
		episode = Episode(narrator)
		episode.write_narrative()
		episode.write_script()
		episode.evalutate()
		if episode.score > bsf_score:
			bsf = episode
			bsf_score = episode.score
	bsf.output_script()
	

if __name__ == '__main__':
	main()