"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:
	This script is used to clean the originally copied and pasted location
	data.  
Notes:
	The way that locations are processed, each word of a multi-word location
	becomes a unique location.  This results in some odd location names, but
	simplifies the locations by ensuring that all of them are just a single
	word.  
"""


file = open('knowledge/locations.txt')

locations = []
locations_so_far = set()
for line in file.readlines():
	as_string = str(line).replace('*', '')
	words = as_string.split()
	for word in words:
		if word not in locations_so_far:
			locations.append(word + '\n')
			locations_so_far.add(word)


write_to = open('knowledge/cleaned_locations.txt', 'w')

for location in locations:
	write_to.write(location)