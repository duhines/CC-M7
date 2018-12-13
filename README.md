# CC-M7
Final Project for Computational Creativity Fall 2018.

System names: personalixca
inspired by the MEXICA system 
locations from the wikipedia page for towns in texas (https://en.wikipedia.org/wiki/List_of_cities_in_Texas)
names from:
	- boys names: http://www.bounty.com/pregnancy-and-birth/baby-names/top-baby-names/100-most-popular-boys-names-so-far-in-2018)
	-girls names: http://www.bounty.com/pregnancy-and-birth/baby-names/top-baby-names/100-most-popular-girls-names-so-far-in-2018

1. Overview: 
	My system is called _personalixca_ in reference to the MEXICA system that
	inspired how the narrative is crafted and one of the features that I 
	focused on: personality modeling.  Script writing is an intensely 
	complicatd problem and I made some simplifying assumptions in order to 
	make the problem more manageable.  Thus, the scripts are represented as a
	simple sequence of actions taken by the characters.  The script generation
	process has three main components represented by different modules: 
	character.py, narrator.py, and action.py.  In general, the narrator module
	keeps track of the locations and characters in the narrative and uses the
	character module (which draws on the action module) to add actions to the 
	narrative.  

2. Setup:
	1. To generate a script, run the `python3 narrator.py` command.
		- the script is written as a .txt file into the results folder.
	2. The character and setting names can be chanced by modifying the 
	cleaned_names and cleaned_locations files in the knowledge folder.

3. 
	I chose to focus on modeling character personality.  Each character is 

	I also modeled the social connections between characters in a way inspired
	by the MEXICA system.  

	The social connection modeling informed how the scripts are evaluated.  The
	fitness of a given script is measured by the total change in the connection 
	parameters between all the characters in the narrative.  For instance, if
	the connections between _character_1_ and _character_2_ was [3, 3, 3, 3] at
	the beginning of the narrative and [2, 2, 2, 2] at the end (each of these 
	numbers represents the magnitude of a type of connection), then the total
	change of the connections would be 4.  

	This system has many opportunites for improvement.  

System Architecture: A more detailed account of your system (at least 4 paragraphs) and its components. You should clearly describe what components of script generation that you chose to focus on (e.g., agent personality modeling, dialogue generation, narrative prose generation, suspense modeling, conflict modeling, musical lyric generation, humor and sarcasm modeling, visual animation, computational cinematography…), citing scholarly work as appropriate. Include a block diagram of your system architecture.
![alt text](https://github.com/duhines/CC-M7/blob/master/personalixca.png "Diagram of System Architecture")

4. 
	PPPP
Computational Creativity: You should follow the general SPECS procedure to evaluate your system. Start by stating your assumptions and definitions for what it means for a system to be creative here. These statements should be founded on prior work (i.e., you should be citing respected scholars in the field). Next, clearly state at least one creativity metric for your system and evaluate it based on that metric. This metric can be derived from the SPECS themes, Ritchie's criteria, the Four PPPPerspectives, or another formalized evaluation procedure from scholarly work (e.g. Colton's Creative Tripod). Regardless of the metric and definitions you specify, you must acknowledge any limitations, biases, or potential issues with your evaluation. Your grade will not be affected if your data is biased or limited unless you leave out this information.

5. 
	Personal Challenges: Describe how you personally challenged yourself on this assignment as a computer scientist. 
	How did you strive to make your system unique, meaningful, and use sophisticated techniques? 
	How did you push yourself as a scholar and a programmer? 
	What new techniques did you try? 
	What discoveries and connections did you make?
