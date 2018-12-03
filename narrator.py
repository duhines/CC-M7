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
class Season: 
	"""
	Purpose: preserve details of characters and setting accross episodes
	"""
	def __init__(self, characters, setting):

class Episode: 
	"""
	Purpose: want to generate episodic narratives, where each follows the 
	rising action, climax, falling action, conclusion narrative structure
	(but perhaps leaving some cliff hangers)


	"""
	def __init__(self, characters, setting):
		self.script = []
		self.characters = characters
		self.setting = setting


	def write_episode(self, num_settings, num_characters, length):
		"""
		Save the episode as a both a text of the script and as a collection of
		the relevant objects 
		"""

		# if we're 

		curr_length = 0
		while curr_length < length:
			# TODO: add ending conditions: all characters die, etc. 



