"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:

Notes:


"""

class Location: 
	def __init__(self, name, characters_at):
		self.name = name
		self.characters_at = characters_at
		self.connected_to = []

	def add_connection(self, location):
		"""
		Purpose: add a connection between one location and another (assuming
		symmetry)
		"""
		self.connected_to.append(location)
		location.connected_to.appen(self)

	def is_present(self, character):
		"""
		Purpose: check if a character is present in a location
		"""
		return character in self.characters_at

class Setting:
	def __init__(self, characters, locations):
		self.locations = locations
		self.characters = characters
		self.current_location
		"""
		Purpose: initialize the setting from a text file of settings
		"""

		# TODO: set up reading the settings from a file.

		# TODO: set up 


	def change_locations(self, new_location):
		"""
		Purpose: change the current location in the story to another location
		in the setting
		"""
		self.current_location = new_location


