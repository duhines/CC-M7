"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:

Notes:
	* personality representation: 
		* -1 to 1 rating of the Big five personality traints
		* and/or -1 to 1 rating of evil->good, chaotic->lawful scale.  

	* perhaps emotions are a modifier for actions:
		* ____ washed the dishes, mod: ANGRILY/SADLY/...
"""


import random
import action as action_stuff

class Personality: 
	"""
	Full good would be a value of 1, Full lawful would be a value of 1
	Full evil would be a value of -1, full chaotic would be a value of -1
	"""
	def __init__(self):
		self.good_evil = self.rand_personality()
		self.lawful_chaotic = self.rand_personality()
		# TODO add the ability fo rpersonalities to change over time
		# self.theta = random.random() + .01
		# self.firmness = random.random()
	
	def rand_personality(self):
		"""
		Purpose: return random value [-1, 1]
		"""
		absolute_value = random.random()
		value = None
		if random.random() < .5:
			value = absolute_value * -1
		else:
			value = absolute_value
		return value

	def __str__(self):
		"""
		Purpose: return string representation of the personality.
		"""
		good = ''
		lawful = ''
		if self.good_evil < -.75:
			good = 'very evil'
		elif self.good_evil < -.5:
			good = 'evil'
		elif self.good_evil < -.25:
			good = 'sort of evil'
		elif self.good_evil < .25 and self.good_evil > -.25:
			good = 'neither good nor evil'
		elif self.good_evil < .5:
			good = 'sort of good'
		elif self.good_evil < .75:
			good = 'good'
		elif self.good_evil < 1:
			good = 'very good'

		lawful = ''
		if self.lawful_chaotic < -.75:
			lawful = 'very chaotic'
		elif self.lawful_chaotic < -.5:
			lawful = 'chaotic'
		elif self.lawful_chaotic < -.25:
			lawful = 'sort of chaotic'
		elif self.lawful_chaotic < .25 and self.lawful_chaotic > -.25:
			lawful = 'neither lawful nor chaotic'
		elif self.lawful_chaotic < .5:
			lawful = 'sort of lawful'
		elif self.lawful_chaotic < .75:
			lawful = 'lawful'
		elif self.lawful_chaotic < 1:
			lawful = 'very lawful'
		return '{} and {}.'.format(good, lawful)
		
	# This would be a big TODO if there was more time
	# def adjust_personality(self, demo_good_evil, demo_lawful_chaotic):
	# 	"""
	# 	Purpose:  If a character ends up making an action that contradicts 
	# 	their personality, then adjust their personality values with 
	# 	respect to this characters personality maleability (theta).  Note,
	# 	characters make actions outside their 
	# 	"""
	# 	self.good_evil = self.demo_good_evil * (1 - self.theta) + demo_good_evil * self.theta
	# 	self.lawful_chaotic = self.lawful_chaotic * (1 - self.theta) + demo_lawful_chaotic * self.theta


class Connection:
	"""
	Purpose: detail the connection between one character and another.  

	Currently using the 4 types model from MEXICA:
		1. brotherly-love / hate
		2. lover's-love / hate
		3. gratefulness / ingratitude
		4. admiration, respect / disdain, disapproval 
	"""
	def __init__(self):
		self.brotherly = self.init_value()
		self.lovers = self.init_value()
		self.gratefulness = self.init_value()
		self.admiration = self.init_value()
		
	def init_value(self):
		"""
		Purpose: return an integer between -3 and 3 for now
		"""	
		absolute_value = random.randint(0, 3)
		value = None
		if random.random() < .5:
			value = absolute_value * -1
		else:
			value = absolute_value

		return value
	
	def adjust_all(self, amount):
		"""
		Purpose: adjust all the connection values.
		"""		
		self.adjust_brotherly(amount)
		self.adjust_lovers(amount)
		self.adjust_gratefulness(amount)
		self.adjust_admiration(amount)

	def adjust_brotherly(self, amount):
		"""
		Purpose: adjust a single connection value.
		"""
		self.brotherly = self.normalize_value(self.brotherly + amount)

	def adjust_lovers(self, amount):
		"""
		Purpose: adjust a single connection value.
		"""
		self.lovers = self.normalize_value(self.lovers + amount)

	def adjust_gratefulness(self, amount):
		"""
		Purpose: adjust a single connection value.
		"""
		self.gratefulness = self.normalize_value(self.gratefulness + amount)

	def adjust_admiration(self, amount):
		"""
		Purpose: adjust a single connection value.
		"""
		self.admiration = self.normalize_value(self.admiration + amount)

	def normalize_value(self, value):
		"""
		Purpose: adjust a value so that it remains in the range[-3, 3]

		TODO: expand this so it doesnt use magic numbers
		"""
		# keep values in the bounds (sorry that these are magic numbers)
		# TODO: flesh out connection system more 
		if value > 3:
			return 3
		if value < -3:
			return -3
		return value

	def get_string(self):
		"""
		Purpose: return a string representation of a connection.
		brotherly-love / hate
		2. lover's-love / hate
		3. gratefulness / ingratitude
		4. admiration, respect / disdain, disapproval
		"""
		string = 'brotherly-love / hate: {}, lover\'s-love / hate: {},' +\
		' gratefulness/ ingratitude: {}, respect / disdain: {}.  '
		return string.format(self.brotherly, self.lovers, self.gratefulness,
			self.admiration)


class SocialNetwork:
	"""
	Purpose: capture characters knowledge of each other and feelings towards the
	other characters.

	Use emotional links inspired by the MEXICA system:

	network = [character1_name->character2_name: connection]

	"""
	def __init__(self, characters):
		self.characters = characters
		self.network = self.generate_network()

	def generate_network(self):
		"""
		Purpose: generate a connection between all the characters
		"""
		network = {}
		for character1 in self.characters:
			all_other_characters = self.characters.copy()
			all_other_characters.remove(character1)
			for character2 in all_other_characters:
				# instantiate with a random connection
				network[character1.name+character2.name] = Connection()
		return network

	def get_connection(self, character1, character2):
		"""
		Purpose: get the connection betweeen two characters.  
		"""
		connection = self.network[character1.name+character2.name]
		return connection

	def for_narrative(self):
		"""
		Purpose: return a string summarizing the characters connections.
		"""
		connection_details = []
		for character1 in self.characters:
			all_other_characters = self.characters.copy()
			all_other_characters.remove(character1)
			for character2 in all_other_characters:
				connection = self.get_connection(character1, character2)
				connection_details.append('Connection from {} to {} is {}'\
					.format(character1.name, character2.name, connection.get_string()))
		return connection_details


class Character:
	def __init__(self, name, personality, goal, health, location):
		self.name = name
		self.personality = personality
		self.goal = goal
		self.health = health
		self.location = location
		self.alive = True
		# TODO: maybe add emotions: self.emotions = emotions

	def __str__(self):
		return self.name

	def __repr__(self):
		return 'Character({}, {}, {}, {}, {})'.format(self.name, self.personality,
			self.goal, self.health, self.location)

	def check_health(self):
		"""
		Purpose: if a character has less than 1 health, then they are dead.
		"""
		if self.health < 1:
			self.alive = False

	def can_act(self, locations, characters, nearby_characters, social_network):
		"""
		Purpose: check to see if this character can do anything.
		"""
		all_actions = action_stuff.Actions(self, locations, characters,
			nearby_characters, social_network).actions
		for action in all_actions:
			if not action.pre_condition:
				all_actions.remove(action)
		if len(all_actions) == 0:
			return False
		return True

	def action_maker(self, locations, characters, nearby_characters, social_network):
		"""
		Purpose: choose an action that works the character towards their goal and is 
		consistent with personality + emotions.
		"""
		self.health -= 5
		self.check_health()
		if not self.alive:
			return '{} has died.'.format(self.name)

		all_actions = action_stuff.Actions(self, locations, characters,
			nearby_characters, social_network).actions
		for action in all_actions:
			if not action.pre_condition:
				all_actions.remove(action)

		if len(all_actions) == 0:
			return '{} does nothing.'.format(self.name)

		act = random.choice(all_actions)
		return act.do()

	def dialogue_maker(self, state):
		return


