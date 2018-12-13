"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:
	Class that allows characters to act.  
	Includes the following classes:
		Actions -
			used to store and initialize all the actions
		Travel -
			implements the possibilities and consequences of a traveling in the
			world
		Injure - 
			implements the consequences of one character injuring another
		Heal - 
			implements the consequences of one character injuring another
		Sleep - 
			implements the consequences of one character sleeping
Notes:
	Any class implementing an action is expected to have a do() method that
	does any book-keeping associated with the action being performed and
	returns a string representing the consequences of the action.
	
	Any action that involves one character impacting another will need to 
	be initialized for all the possible recipients of the action in the 
	get_actions function in Actions.

	The path_finding function for the Traveling class currently assumes that
	all the places are connected--this would need to be update with some kind
	of path finding algorithm if every location was not connected to every 
	other location. 

	Sometimes, the justification function will be called when the clauses in
	question are all false.  No idea why this happens, but it shoudn't.
"""


import random
from random import choice


class Actions:
	"""
	Class used to store all the actions available to a character.
	Implements the following method:
		get_actions
	"""
	def __init__(self, character, locations, characters, nearby_characters, social_network):
		self.character = character
		self.locations = locations
		self.characters = characters
		self.nearby_characters = nearby_characters
		self.social_network = social_network
		self.actions = self.get_actions()

	def get_actions(self):
		"""
		Purpose: return the actions available for a character
		"""
		# get list of characters that the acting character can interact with
		other_characters = self.nearby_characters.copy()
		if self.character in other_characters:
			other_characters.remove(self.character)
		
		actions = []
		actions.append(Travel(self.character, self.locations))
		actions.append(Sleep(self.character))

		# since we can heal/injure other characters, we need an action for each 
		# possible character that can be a recipient of one of these actions
		for character2 in other_characters:
			actions.append(Injure(self.character, character2, self.social_network))
			actions.append(Heal(self.character, character2, self.social_network))

		return actions


class Travel:
	"""
	Class that implements a traveling action.  
	"""
	def __init__(self, character, locations):
		self.character = character
		self.locations = locations
		self.pre_condition = self.character.health > 30

	def do(self):
		"""
		Purpose: either travel randomly or travel due to characters goal
		"""
		character = self.character 
		locations = self.locations
		if self.character.goal != None:
			if self.character.goal.place != None:
				character.location = self.path_find(character.goal.place)
				return character.name + ' traveled to ' + character.location + \
				'in order to ' + character.goal.statement
		else:
			options = self.locations['names'].copy()
			options.remove(self.character.location)
			if len(options) == 0:
				return '{} wanders around {}.'.format(self.character.name,
					self.character.location)
			character.location = choice(options)
			return character.name + ' travels to ' + character.location
		
	def path_find(self, goal):
		"""
		Purpose: if all places were not connected, then we would need to figure
		out how to get to where we want to go.  

		TODO: extend this to work when there is not an edge between every 
		location!
		"""
		return goal



class Injure:
	"""
	Class that implements the injure action.
	"""
	def __init__(self, character1, character2, social_network):
		self.character1 = character1
		self.character2 = character2
		self.social_network = social_network
		self.clause1 = character1.personality.lawful_chaotic < -.5
		self.clause2 = character1.personality.good_evil < -.5
		self.clause3 = social_network.get_connection(character1, character2).brotherly < -1
		self.clause4 = social_network.get_connection(character1, character2).lovers < -1
		self.clause5 = character2.health > 1
		self.pre_condition = (self.clause1 or self.clause2 or self.clause3 or self.clause4) and self.clause5

	def do(self):
		"""
		Purpose: one character injures another.
		"""
		# TODO change this so that more animosity results in greater injury
		damage = random.randint(10, 50)
		self.character2.health -= damage
		if damage < 30:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(-1)
			return '{} injures {} because {}.'.format(self.character1.name, 
				self.character2.name, self.get_justification())
		else:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(-2)
			return '{} significantly injures {} because {}.'.format(
				self.character1.name, self.character2.name, self.get_justification())

	def get_justification(self):
		"""
		Purpose: return a string representing the clause that allowed this
		action to happen.
		"""
		if self.clause1:
			return '{} is chotic'.format(self.character1.name)
		elif self.clause2:
			return '{} is evil'.format(self.character1.name)
		elif self.clause3:
			return '{} feels brotherly hate towards {}'.format(
				self.character1.name, self.character2.name)
		elif self.clause4:
			return '{} feels lover\'s hate towards {}'.format(
				self.character1.name, self.character2.name)
		else:
			return '{} made a mistake'.format(self.character1.name)


class Heal:
	"""
	Class for the heal action.
	"""
	def __init__(self, character1, character2, social_network):
		self.character1 = character1
		self.character2 = character2
		self.social_network = social_network
		self.clause1 = character1.personality.lawful_chaotic > .5
		self.clause2 = character1.personality.good_evil > .5
		self.clause3 = social_network.get_connection(character1, character2).brotherly >= 1
		self.clause4 = social_network.get_connection(character1, character2).lovers >= 1
		self.clause5 = character2.health < 100 and self.character2.health > 0
		self.pre_condition = (self.clause1 or self.clause2 or self.clause3 or self.clause4) and self.clause5

	def do(self):
		"""
		Purpose: one character heals another character
		"""
		heal = random.randint(10, 50)
		self.character2.health += heal
		if heal < 30:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(1)
			return '{} heals {} because {}.'.format(self.character1.name, 
				self.character2.name, self.get_justification())
		else:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(2)
			return '{} significantly heals {} because {}.'.format(
				self.character1.name, self.character2.name, self.get_justification())

	def get_justification(self):
		"""
		Purpose: return a string representing the clause that allowed this
		action to happen.
		"""

		if self.clause1:
			return '{} is lawful'.format(self.character1.name)
		elif self.clause2:
			return '{} is good'.format(self.character1.name)
		elif self.clause3:
			return '{} feels brotherly love towards {}'.format(
				self.character1.name, self.character2.name)
		elif self.clause4:
			return '{} feels lover\'s love towards {}'.format(
				self.character1.name, self.character2.name)
		else:
			return '{} made a mistake'.format(self.character1.name)
	

class Sleep:
	"""
	Class for the sleep action.  
	"""
	def __init__(self, character):
		self.character = character
		self.pre_condition = self.character.health > 20

	def do(self):
		"""
		Purpose: sleep to regain some health.
		"""
		self.character.health += 30
		return '{} sleeps to regain some strength.'.format(self.character.name)


