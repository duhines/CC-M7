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


import random as rando


class Personality: 
	def __init__(self, good_evil, lawful_chaotic, theta, firmness):
		self.good_evil = good_evil
		self.lawful_chaotic = lawful_chaotic
		self.theta = theta
		self.firmness = firmness
	
	def adjust_personality(self, demo_good_evil, demo_lawful_chaotic):
		"""
		Purpose:  If a character ends up making an action that contradicts 
		their personality, then adjust their personality values with 
		respect to this characters personality maleability (theta).  Note,
		characters make actions outside their 
		"""
		self.good_evil = self.demo_good_evil * (1 - self.theta) + demo_good_evil * self.theta
		self.lawful_chaotic = self.lawful_chaotic * (1 - self.theta) + demo_lawful_chaotic * self.theta


class Connection:
	"""
	Purpose: detail the connection between one character and another.  

	Currently using the 4 types model from MEXICA:
		1. brotherly-love / hate
		2. lover's-love / hate
		3. gratefulness / ingratitude
		4. admiration / respect
		5. disdain / disapproval 
	"""
	def __init__(self):
		self.brotherly_love_hate = self.init_value()
	
	def init_value(self):
		"""
		Purpose: return an integer between -3 and 3 for now
		"""	
		absolute_value = random.randint(0, 3)
		if random.random() < .5:
			value = absolute_value * -1
		else:
			value = absolute_value

		return absolute_value


class SocialNetwork:
	"""
	Purpose: capture characters knowledge of each other and feelings towards the
	other characters.

	Use emotional links inspired by the MEXICA system:

	network = [character1_name->character2_name: connection]

	"""
	def __init__(self, characters):
		self.network = self.generate_network()


class Character:
	def __init__(self, name, personality, goal, social_network, health, emotions):
		self.name = name
		self.personality = personality
		self.goal = goal
		self.social_network = social_network
		self.health = health
		self.emotions = emotions

	def action_maker(self, state):
		"""
		Purpose: choose an action that works the character towards their goal and is 
		consistent with personality + emotions
		"""

		return action

	def dialogue_maker(self, state):



