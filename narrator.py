"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:

Notes:
	* output will be a text script of TV episodes (maybe build this up to
	seasons?)

"""

import random
import knowledge as knows
import character
from random import choice


NUM_CHARACTERS = 2
NUM_LOCATIONS = 1
RATE_LOCATION_CONNECTED = 1
NUM_ACTIONS = 5


class Narrator:
	def __init__(self):
		self.knowledge = knows.Knowledge()
		self.locations = self.init_locations()
		self.characters = self.init_characters()
		self.current_location = choice(self.locations['names'])
		self.social_network = character.SocialNetwork(self.characters)

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
		print('changing location')
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
	Keep track of the time that an event occured during.
	"""
	def __init__(self, time, action):
		self.time = time
		self.action = action


class Season: 
	"""
	Purpose: preserve details of characters and setting accross episodes
	"""
	def __init__(self, characters, setting):
		return 


class Episode: 
	"""
	Purpose: want to generate episodic narratives, where each follows the 
	rising action, climax, falling action, conclusion narrative structure
	(but perhaps leaving some cliff hangers)


	"""
	def __init__(self, narrator, num_actions=NUM_ACTIONS):
		self.narrator = narrator
		self.narrative = []
		self.script = []
		self.num_actions = num_actions
		self.time = 0

	def write_narrative(self):
		"""
		Purpose: determine the sequences of actions that make up the script.   
		"""

		# if we're 
		narrator = self.narrator
		curr_acts = 0
		events = []
		opener = 'We begin our story in {}.  '.format(narrator.current_location)
		for character in narrator.characters_at(narrator.current_location):
			opener += '{} is here.  '.format(character)

		initial_social_structre = narrator.social_network.for_narrative()
		print(initial_social_structre)
		for line in initial_social_structre:
			opener += line
		events.append(Event(0, opener))
		while curr_acts < self.num_actions:
			# want to only be focused on locations where there are characters than
			# can do things
			possible_characters = narrator.characters_at(narrator.current_location)
			can_act = narrator.can_act(possible_characters)
			print('current location {}'.format(narrator.current_location))
			print('characters here {}'.format(possible_characters))
			print('can act {}'.format(can_act))
			if len(can_act) == 0:
				print('need to change location--------')
				change_narrative_location = narrator.change_location()
				events.append(Event(self.time, change_narrative_location))
				if change_narrative_location == 'There are no characters left.':
					# the story is OVER
					break
			else:
				next_actor = choice(can_act)
				act = next_actor.action_maker(narrator.locations, 
					narrator.characters, possible_characters, narrator.social_network)
				print(act)
				events.append(Event(self.time, act))
				curr_acts += 1

			self.time += 1

		closer = 'And thus ends the episode.  '
		end_social_structre = narrator.social_network.for_narrative()
		for line in end_social_structre:
			closer += line
		events.append(Event(self.time, closer))
		self.narrative = events

	def write_script(self):
		"""
		Purpose: from a list of actions, 
		"""
		for event in self.narrative:
			self.script.append(self.get_narrative_from_action(event))


	def get_narrative_from_action(self, event):
		"""
		Purpose: translate 
		"""
		
		# TODO: set up way of getting narrative form 
		return str(event.action.strip())


def main():
	narrator = Narrator()
	for character in narrator.characters:
		print('name: {}'.format(character.name))
		print('personality: {}'.format(character.personality))
		print('goal: {}'.format(character.goal))
		print('health: {}'.format(character.health))
		print('location: {}'.format(character.location))

	episode = Episode(narrator)
	episode.write_narrative()
	episode.write_script()
	print(episode.script)
if __name__ == '__main__':
	main()