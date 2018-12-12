
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