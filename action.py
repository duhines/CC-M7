"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:

Notes:


"""

# class Action: 
# 	"""
# 	name 
# 	"""
# 	def __init__(self, name, personality, pre_conditions, post_conditions, impact, characters, num_characters):
# 		self.num_characters = num_characters
# 		self.name = name
# 		# list of characters involved in the action in logical order 
# 		self.characters = characters
# 		# the personality values typical of this kind of action
# 		self.personality = personality # personality is defined as a range for each
# 		# personality attribute where this act is appropiate for a personality with
# 		# values falling into that range
# 		self.pre_conditions = pre_conditions
# 		self.post_conditions = post_conditions
# 		self.impact = impact


import random
from random import choice


class Actions:
	def __init__(self, character, locations, characters, nearby_characters, social_network):
		self.character = character
		self.locations = locations
		self.characters = characters
		self.nearby_characters = nearby_characters
		self.social_network = social_network
		self.actions = self.get_actions()

	def get_actions(self):
		"""
		Purpose: return the actions for a character
		"""
		# get list of characters that the acting character can interact with
		other_characters = self.nearby_characters.copy()
		if self.character in other_characters:
			other_characters.remove(self.character)
		
		actions = []
		actions.append(Travel(self.character, self.locations))
		actions.append(Sleep(self.character))

		for character2 in other_characters:
			actions.append(Injure(self.character, character2, self.social_network))
			actions.append(Heal(self.character, character2, self.social_network))

		return actions


# create a class for all the actions
class Travel:
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
	def __init__(self, character1, character2, social_network):
		self.character1 = character1
		self.character2 = character2
		self.social_network = social_network
		clause1 = self.character1.personality.lawful_chaotic < -.5
		clause2 = self.character1.personality.good_evil < -.5
		clause3 = self.social_network.get_connection(character1, character2).brotherly < -1
		clause4 = self.social_network.get_connection(character1, character2).lovers < -1
		clause5 = self.character2.health > 1
		self.pre_condition = (clause1 or clause2 or clause3 or clause4) and clause5

	def do(self):
		"""
		Purpose: one character injures another.
		"""
		# TODO change this so that more animosity results in greater injury
		damage = random.randint(10, 50)
		self.character2.health -= damage
		if damage < 30:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(-1)
			return '{} injures {}.'.format(self.character1.name, 
				self.character2.name)
		else:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(-2)
			return '{} significantly injures {}.'.format(
				self.character1.name, self.character2.name)


class Heal:
	def __init__(self, character1, character2, social_network):
		self.character1 = character1
		self.character2 = character2
		self.social_network = social_network
		clause1 = self.character1.personality.lawful_chaotic > .5
		clause2 = self.character1.personality.good_evil > .5
		clause3 = self.social_network.get_connection(self.character1, self.character2).brotherly > 1
		clause4 = self.social_network.get_connection(self.character1, self.character2).lovers > 1
		clause5 = self.character2.health < 100 and self.character2.health > 0
		self.pre_condition = (clause1 or clause2 or clause3 or clause4) and clause5

	def do(self):
		"""
		Purpose: one character heals another character
		"""
		heal = random.randint(10, 50)
		self.character2.health += heal
		if heal < 30:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(1)
			return '{} heals {}.'.format(self.character1.name, self.character2.name)
		else:
			self.social_network.get_connection(self.character2, self.character1).adjust_all(2)
			return '{} significantly heals {}.'.format(self.character1.name, self.character2.name)


class Sleep:
	def __init__(self, character):
		self.character = character
		self.pre_condition = self.character.health > 20

	def do(self):
		"""
		Purpose: sleep to regain some health.
		"""
		self.character.health += 30
		return '{} sleeps to regain some strength.'.format(self.character.name)


