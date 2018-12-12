"""
Purpose:
	This script is used to clean the originally copied and pasted location
	data.  
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