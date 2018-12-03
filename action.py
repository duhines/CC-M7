"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:

Notes:


"""

class Action: 
	"""
	name 
	"""
	def __init__(self, name, personality, pre_conditions, post_conditions, impact, characters):
		self.name = name
		self.characters = characters
		# the personality values typical of this kind of action
		self.personality = personality # personality is defined as a range for each
		# personality attribute where this act is appropiate for a personality with
		# values falling into that range
		self.pre_conditions = pre_conditions
		self.post_conditions = post_conditions
		self.impact = impact


	def get_narrative_from_action(self):
		"""
		Purpose: translate 
		"""

		# TODO: set up way of getting narrative form 


class Actions:
	# TODO: initialize actions from a knowledge base of actions
	def __init__(self):
		self.actions = get_actions()

	def get_actions(self):
		travel = Action('travels', [[-1, 1][-1, 1]], )
