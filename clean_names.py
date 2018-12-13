"""
Author: Dustin Hines
Course: Computational Creativity Fall 2018
Project: M7: Playing with Words
Date: last modified 12/13
Description:
	This is a script to clean names.  The names are from the top 100 boys
	and girls names from 2018 from bounty.com

Notes: 
	Assumes the format of the original names file has the name first on 
	each line.
"""
file = open('knowledge/names.txt')

cleaned = []
for line in file.readlines():
	if line == '\n':
		continue
	cleaned_name = line.split()[0]
	cleaned.append(cleaned_name + '\n')

file.close()

cleaned_file = open('knowledge/cleaned_names.txt', 'w')

for name in cleaned:
	cleaned_file.write(name)

cleaned_file.close()