import os
import csv
import pickle
import calendar
from random import randint
from datetime import datetime
from Character import Character
from Combat import Combat

'''
	TODO: ability to manually rearrange initiative order
'''
# ############## #
# Test functions #
# ############## #		
def test_combat():
	f = open('test_combat.txt', 'r')
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters(f))
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	combatants = tiebreaker(combatants)
	combat = round_order(combatants, None, f)
	write_combat_to_file(combat)
	f.close()

def test_tiebreak():
	f = open('test_tiebreak.txt', 'r')
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters(f))
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	combatants = tiebreaker(combatants)
	f.close()

# ####################### #
# Combatant instantiation #
# ####################### #
def player_characters():
	'''Create list of Character objects to represent the player characters

	Returns
	-------
	pcs : list
		list of Character objects
	'''

	pc_list = ['Dennis Le Menace', 'Pierre', 'Ronan', 'Dame Romaine']
	pcs = []
	for pc in pc_list:
		# pc_init = int(randint(1,20))
		# pc_init = 0
		# if pc == 'Dennis Le Menace':
		# 	pc_init = 5
		# elif pc == 'Pierre':
		# 	pc_init = 21
		# elif pc == 'Ronan':
		# 	pc_init = 21
		# elif pc == 'Dame Romaine':
		# 	pc_init = 14
		pc_init = get_quantity_input('{} initiative roll: '.format(pc))
		pc_dex_bonus = get_dex_bonus(pc)
		pcs.append(Character(pc, pc_init, pc_dex_bonus))
	return pcs

def nonplayer_characters(f=False):
	'''Ask user for monsters in combat. Create list of Character objects containing each monster.

	Parameters
	----------
	f : file object (optional)
		file used for testing

	Returns
	-------
	npc_list : list
		list of Character objects
	'''

	npc_name = ''
	npc_list = []
	while True:
		if f:
			#testing
			npc_name = f.readline().strip()
		else:
			npc_name = input('Monster name: ')
		if len(npc_name) < 2:
			print()
			break
		if f:
			#testing
			num_npc = int(f.readline().strip())
			dex_bonus = int(f.readline().strip())
		else:
			num_npc = get_quantity_input('Number of ' + npc_name + 's: ')
			dex_bonus = get_dex_bonus(npc_name)
		if num_npc > 1:
			for i in range(num_npc):
				# add consecutive numbers after each npc name
				npc_multi = npc_name + str(i+1)
				npc_list.append(Character(npc_multi, get_npc_init(dex_bonus), dex_bonus, False))
		else:
			npc_list.append(Character(npc_name, get_npc_init(dex_bonus), dex_bonus, False))
	return npc_list

# ############### #
# 'Get' functions #
# ############### #

def get_dex_bonus(char_name):
	'''Get the dexterity bonus of a character either from a file or user input. 
	Also, since this file checks if a character exists in monster.csv, it calls the function to add new characters to the file.

	Parameters
	----------
	char_name : str
		Name of character who's dexterity bonus is required

	Returns
	-------
	dex_bonus : int
		Number representing the dexterity bonus of the character
	'''

	monster_file = open('monsters.csv', 'r')
	monsters = csv.reader(monster_file)
	for monster_row in monsters:
		if monster_row[0] == char_name.lower():
			return int(monster_row[1])
	monster_file.close()
	dex_bonus = get_quantity_input(char_name + ' dex bonus: ')
	add_monster = get_yes_no_input('Save monster to file [y/n]: ')
	if add_monster == 'y':
		add_character_to_file([char_name.lower(), dex_bonus])
	return dex_bonus
	
def get_npc_init(dex_bonus):
	'''Return a random number between 1 and 20 plus dexterity bonus.

	Parameters
	----------
	dex_bonus : int
		dexterity bonus

	Returns
	-------
	int
		number representing the initiative count
	'''

	return int(randint(1,20) + dex_bonus)

def get_quantity_input(input_message):
	'''A function to get the verify an integer input from the user. Will loop until integer entered.

	Parameters
	----------
	input_message : str
		Message to be display to the user

	Returns
	-------
	: int
		an integer given by the user
	'''

	while True:
		try:
			return int(input(input_message))
		except ValueError:
			print('Invalid input - please enter a number.')

def get_file_name_input():
	'''A function to get the name of the combat, which forms part of a file name and, therefore, requires special rules.
	Loops until user input is valid.

	Returns
	-------
	combat_name : str
		Name of the combat
	'''

	illegal_chars = ['<', '>', ':', '\"', '/', '\\', '|', '?', '*']
	while True:
		combat_name = input('Name of combat: ')
		combat_name_contains_illegal_chars = sum(c in illegal_chars for c in combat_name)
		if combat_name_contains_illegal_chars == 0:
			return combat_name
		else:
			print('Illegal input - combat name may not contain any of the following characters:')
			print('<  >  :  \"  /  \\  |  ?  *')

def get_yes_no_input(input_message):
	'''A function to get a yes or no response from the user. Loops until user input is valid.

	Parameters
	----------
	input_message : str
		Message to be display to the user

	Returns
	-------
	y/n: str
		A string representing the user's selection
	'''

	while True:
		response = input(input_message).lower()
		if response == 'y' or response == 'yes':
			return 'y'
		elif response == 'n' or response == 'no':
			return 'n'
		else:
			print('Invalid input - use \'y\' or \'n\'')			

def get_list_selection_input(list_length, input_message='Your input: '):
	'''A function to verify a user's input when selecting options from a list (e.g. selecting previous combats).

	Parameters
	----------
	list_length : int
		The number of elements in the list

	input_message : str (optional)
		Message to be display to the user

	Returns
	-------
	selection: int
		A number corresponding to one of the options presented to the user
	'''

	while True:
		try:
			selection = int(input(input_message))
			if selection > 0 and selection <= list_length:
				return selection
			else:
				print('Invalid input - please enter a number between 1 and {}.'.format(list_length))
		except ValueError:
			print('Invalid input - please enter a number between 1 and {}.'.format(list_length))

def get_new_or_existing_combat_input():
	'''A function to verify a user's input for new or existing combat. Loops until valid input found.

	Returns
	-------
	n/e: str
		A string representing the user's selection
	'''

	while True:
		new_or_existing = input('\nCombat:\n1) [N]ew\n2) [E]xisting\n: ').lower()
		if new_or_existing == 'n' or new_or_existing == 'new' or new_or_existing == '1':
			return 'n'
		elif new_or_existing == 'e' or new_or_existing == 'existing' or new_or_existing == '2':
			return 'e'
		else:
			print('Invalid input - use \'n\' or \'e\'')

# ######################## #
# Combat-related functions #
# ######################## #

def create_combat(combatants, f=False):
	'''Instantiate a combat object.

	Parameters
	----------
	combatants : list
		List of character objects particpating in the combat
	f : file object (optional)
		file used for testing

	Returns
	-------
	combat : Combat object
		A Combat object
	'''

	if f:
		combat_name = f.readline().strip()
		print('Combat name: ', combat_name)
	else:
		combat_name = get_file_name_input()
	print('Combat name: ', combat_name)	
	# create combat object
	combat = Combat(combat_name)
	# add combatants to combat object
	for combatant in combatants:
		combat.combatants.append(combatant)
	return combat

def print_initiative_order(combatants):
	'''A function to print out the initiative order of the combat.

	Parameters
	----------
	combatants : list
		List of character objects particpating in the combat
	'''

	print('INITIATIVE ORDER:')
	for char in combatants:
		if char.roll_off == 0:
			print('{}: {} ({})'.format(char.initiative, char.name, char.dex_bonus))
		else:
			print('{}: {} ({}) - ROLL OFF={}'.format(char.initiative, char.name, char.dex_bonus, char.roll_off))
	print()

def round_order(combatants, combat=None, f=False):
	'''Loop through the combatants in a combat, simulating a D&D combat encounter.

	Parameters
	----------
	combatants : list
		List of character objects particpating in the combat
	combat : Combat object (optional)
		A Combat object
	f : file object (optional)
		file used for testing

	Returns
	-------
	combat : Combat object
		A Combat object
	'''

	print_initiative_order(combatants)
	round = 0
	round_dict = {}
	if not combat:
		combat = create_combat(combatants, f)
		round = 1
	else:
		# resume existing combat
		round = max(combat.rounds, key=int) + 1
		
	# Loop through rounds of combat
	while True:
		round_dict[round] = {} # {1:{'Ronan': 'hit goblin for 2 dmg', 'Pierre'...}, 2:{}}
		print('========================')
		print('========================')
		print('======= ROUND {} ========'.format(str(round)))
		print('========================')
		print('========================')
		for i in range(len(combatants)):
			print(combatants[i].name + '\'s turn')
			if f:
				round_dict[round][combatants[i].name] = f.readline().strip()
				print('action: ', round_dict[round][combatants[i].name])
			else:
				round_dict[round][combatants[i].name] = input(': ')
		print('ROUND ' + str(round) + ' END')
		if f:
			over = f.readline().strip()
			print('Combat over [y/n]: ', over)
		else:
			over = get_yes_no_input('Combat over [y/n]: ')
		if over == 'y':
			combat.add_round(round_dict)
			break
		combat.add_round(round_dict)
		round += 1
	return combat

def tiebreaker(combatants):
	'''A function to break ties between characters' initiative counts and, if necessary, their dexterity bonuses.
	TODO: reduce duplicate code

	Parameters
	----------
	combatants : list
		List of character objects particpating in the combat

	Returns
	-------
	combatants : list
		List of character objects particpating in the combat, in correct order
	'''

	tie_start_ind = 0
	tie_end_ind = 0
	print_initiative_order(combatants)
	for i in range(len(combatants)):
		# get start and end indices of tied combatants in list
		# sort each tie set by dex bonus
		end_found = False
		if i < len(combatants)-1:
			if combatants[i].initiative == combatants[i+1].initiative and i == 0:
				tie_start_ind = i
			elif combatants[i].initiative == combatants[i+1].initiative and combatants[i].initiative != combatants[i-1].initiative:
				tie_start_ind = i
		if i > 0 and i < len(combatants)-1:
			if combatants[i].initiative != combatants[i+1].initiative and combatants[i].initiative == combatants[i-1].initiative:
				tie_end_ind = i
				end_found = True
		if combatants[i].initiative == combatants[i-1].initiative and i == len(combatants)-1:
			tie_end_ind = i
			end_found = True
		if end_found:
			print('TIEBREAKER at {}'.format(combatants[tie_start_ind].initiative))
			combatants[tie_start_ind:tie_end_ind+1] = sorted(combatants[tie_start_ind:tie_end_ind+1], key=lambda x:x.dex_bonus, reverse=True) 
			print('Between: ' + ', '.join([x.name for x in combatants[tie_start_ind:tie_end_ind+1]]))
			# search through the tied initiative set looking for tied dex bonuses
			dex_bonus_tie_start_ind = 0
			dex_bonus_tie_end_ind = 0
			print_initiative_order(combatants)
			for j in range(tie_start_ind, tie_end_ind+1):
				# print('j: {}, tie_start:end {}:{}'.format(j, tie_start_ind, tie_end_ind))
				dex_bonus_end_found = False
				if j < tie_end_ind:
					if combatants[j].dex_bonus == combatants[j+1].dex_bonus and j == tie_start_ind:
						dex_bonus_tie_start_ind = j
					elif combatants[j].dex_bonus == combatants[j+1].dex_bonus and combatants[j].dex_bonus != combatants[j-1].dex_bonus:
						dex_bonus_tie_start_ind = j
				if j > tie_start_ind and j < tie_end_ind:
					if combatants[j].dex_bonus != combatants[j+1].dex_bonus and combatants[j].dex_bonus == combatants[j-1].dex_bonus and combatants[j].initiative == combatants[j-1].initiative:
						dex_bonus_tie_end_ind = j
						dex_bonus_end_found = True
				if combatants[j].dex_bonus == combatants[j-1].dex_bonus and j == tie_end_ind:
					dex_bonus_tie_end_ind = j
					dex_bonus_end_found = True
				if dex_bonus_end_found:
					print('ROLL OFF at {} dex bonus'.format(combatants[dex_bonus_tie_start_ind].dex_bonus))
					for m in combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1]:
						if not m.pc:
							m.roll_off = int(randint(1,20))
							print('{} roll: {}'.format(m.name, m.roll_off))
						else:
							m.roll_off = get_quantity_input('{} roll: '.format(m.name))
					combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1] = sorted(combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1], key=lambda x:x.roll_off, reverse=True)
					print_initiative_order(combatants)
	return combatants	

# ############# #
# File handling #
# ############# #

def write_combat_to_file(combat):
	'''A function which creates a file with a unique name that stores a serialized combat object.

	Parameters
	----------
	combat : Combat object
		A Combat object
	'''

	print('Saving {} to file'.format(combat.name))
	filename = datetime.now().strftime('%Y%m%d_%H%M%S_{}.pickle'.format(combat.name.replace(' ','_')))
	directory = 'combats'
	path = directory + '/' + filename
	try:
		with open(path, 'wb') as f:
			pickle.dump(combat, f)
	except Exception as e:
		print('Exception: ', e)

def add_character_to_file(new_character):
	'''Add row containing character name and dexterity bonus to csv file.

	Parameters
	----------
	new_monster : list
		list containing two elements: character name and character dexterity bonus
	'''

	with open('monsters.csv', 'a', newline='') as csvfile:
		csv_writer = csv.writer(csvfile)
		csv_writer.writerow(new_character)

def get_combat_file(return_file=False, date_time=()):
	'''A function which returns combat file information (combat name, date, time) from a directory.

	Parameters
	----------
	return_file : boolean (optional, I think this parameter is unnecessary)
		Flag whether or not to return the file
	date_time : tuple
		tuple elements consisting of the date and time

	Returns
	-------
	file_info : list
		List of lists. The inner lists are comprised of a combat file name, date, and time.
	'''

	file_info = []
	directory = os.fsdecode('combats')
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		date_and_time = [filename[0:8], filename[9:15]] # returns ['20220721', '204351']
		if return_file and date_time:
			if date_time[0] == date_and_time[0] and date_time[1] == date_and_time[1]:
				return filename
		index_of_period = filename.index('.')
		file_combat_name = filename[16:index_of_period].replace('_', ' ')
		date_and_time.append(file_combat_name)
		file_info.append(date_and_time)
	return sorted(file_info, key=lambda file_info:[file_info[0],file_info[1]], reverse=True)

def display_combat_options(num_battles_displayed, gui=False):
	'''A function which displays 'num_battles_displayed' most recent combats and asks the user to make a selection.

	Parameters
	----------
	num_battles_displayed : int
		The number of most recent combats to be displayed

	Returns
	-------
	Combat : Combat Object
		Deserialized user selected file
	'''

	file_info = get_combat_file() # [['20220725', '081517', 'battle of later that afternoon'],..]
	
	combat_selection_dict = {1: '', 2: '', 3: ''}
	file_selection_dict = {1: '', 2: '', 3: ''}
	i = 1
	for combat_file in file_info[0:num_battles_displayed]:
		combat_name = combat_file[2].title()
		combat_date = combat_file[0][0:4] + '/' + calendar.month_abbr[int(combat_file[0][4:6])] + '/' + combat_file[0][6:8]
		combat_time = combat_file[1][0:2] + ':' + combat_file[1][2:4] + ':' + combat_file[1][4:6]
		combat_select = combat_name + ' [' + combat_date + ' ' + combat_time + ']'
		combat_selection_dict[i] = combat_select
		file_selection_dict[i] = (combat_file[0], combat_file[1])
		i+=1
	if gui:
		return combat_selection_dict, file_selection_dict
	print('Select from the {} most recent battles:'.format(num_battles_displayed))
	for k, v in combat_selection_dict.items():
		print(str(k) + ') ', v)
	selection_input = get_list_selection_input(num_battles_displayed, '\nSelect a combat by list number: ')
	selection = combat_selection_dict[selection_input]
	print('You have selected: ' + selection)
	return selection_input, file_selection_dict

def get_combat_based_on_selection(selection_input, file_selection_dict):
	selected_file = file_selection_dict[selection_input]
	combat_file = get_combat_file(True, selected_file)
	with open('combats/' + combat_file, 'rb') as f:
		return pickle.load(f)

def read_pickled_combat_file():
	'''A function to print the contents of a combat file.
	'''
	selection_input, file_selection_dict = display_combat_options(5)
	combat = get_combat_based_on_selection(selection_input, file_selection_dict)
	combat.print_combat()
	for combatant in combat.combatants:
		if combatant:
			combatant.print_character()

# ################## #
# Start your engines #
# ################## #

def resume_combat():
	'''A function to resume a combat from a file
	'''

	selection, selected_file = display_combat_options(3)
	combat = get_combat_based_on_selection(selection, selected_file)
	combat = round_order(combat.combatants, combat)
	write_combat_to_file(combat)

def start_combat():
	'''A function to start a new combat
	'''
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters())
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	combatants = tiebreaker(combatants)
	combat = round_order(combatants)
	write_combat_to_file(combat)

def main():
	'''A function to ask the user if they want to start a new combat or continue a saved combat from a file
	'''
	new_or_existing = get_new_or_existing_combat_input()
	if new_or_existing == 'n':
		start_combat()
	else:
		resume_combat()
	
if __name__ == '__main__':
	main()
	# test_tiebreak()
	# test_combat()
	# resume_combat()
	# read_pickled_combat_file()
	