"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:
	File to set up knowledge by reading in information from a names and
	locations file in the knowledge base.  
Notes:
	Assumes that the names and locations file are a each a series
	of items separated by a newline.  
"""


LOCATIONS_FILE = 'cleaned_locations.txt'
NAMES_FILES = 'cleaned_names.txt'
ACTIONS_FILE = 'actions.json'
EXTENTION = 'knowledge/'


class Knowledge:
	def __init__(self):
		self.names = self.get_names()
		self.locations = self.get_locations()

	def get_names(self):
		"""
		Purpose: read in names from the cleaned_names files and save them 
		in a list object. 
		"""
		file = open(EXTENTION + NAMES_FILES)
		names = [] 
		for line in file.readlines():
			names.append(line.strip())

		return names

	def get_locations(self):
		"""
		Purpose: read in the locations from the cleaned_locations file and 
		load them into a list object.
		
		The relationship between locations will be established by the narrator.
		"""
		file = open(EXTENTION + LOCATIONS_FILE)
		locations = []
		for line in file.readlines():
			locations.append(line.strip())

		return locations
