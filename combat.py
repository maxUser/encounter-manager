import os
import csv
import sys
import pickle
import calendar
from random import randint
from datetime import datetime


'''
	TODO: input error checking
	TODO: save combat in progress and resume where it left off
	TODO: ask to add new monsters to monsters.csv
	TODO: ability to manually rearrange initiative order
'''

class Character:
	def __init__(self, name, initiative, dex_bonus=0, pc=True):
		self.name = name
		self.initiative = initiative
		self.dex_bonus = dex_bonus
		self.pc = pc
		self.roll_off = 0	
	def print_character(self):
		print('{}\n\tinitiative: {} [{}]'.format(self.name, self.initiative, self.dex_bonus))

class Combat:
	def __init__(self, name):
		self.name = name
		self.rounds = {}
		self.combatants = []
	def add_round(self, round):
		self.rounds.update(round)
	def print_combat(self):
		print(self.name)
		for k, v in self.rounds.items():
			print(k, v)
		
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

def player_characters():
	pc_list = ['Dennis Le Menace', 'Pierre', 'Ronan', 'Dame Romaine']
	pcs = []
	for pc in pc_list:
		pc_init = int(randint(1,20))
		# pc_init = 0
		# if pc == 'Dennis Le Menace':
		# 	pc_init = 5
		# elif pc == 'Pierre':
		# 	pc_init = 21
		# elif pc == 'Ronan':
		# 	pc_init = 21
		# elif pc == 'Dame Romaine':
		# 	pc_init = 14
		# pc_init = get_quantity_input('{} initiative roll: '.format(pc))
		pc_dex_bonus = get_dex_bonus(pc)
		pcs.append(Character(pc, pc_init, pc_dex_bonus))
	return pcs

def get_quantity_input(something):
	while True:
		try:
			return int(input(something))
		except ValueError:
			print('Invalid input, please enter a number.')

def nonplayer_characters(f=False):
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

def get_dex_bonus(char_name):
	dex_bonus = 0
	monster_file = open('monsters.csv', 'r')
	monsters = csv.reader(monster_file)
	for monster_row in monsters:
		if monster_row[0] == char_name.lower():
			return int(monster_row[1])
	monster_file.close()
	dex_bonus = get_quantity_input(char_name + ' dex bonus: ')
	return dex_bonus
	
def get_npc_init(dex_bonus):
	return int(randint(1,20) + dex_bonus)
 
def print_initiative_order(combatants):
	print('INITIATIVE ORDER:')
	for char in combatants:
		if char.roll_off == 0:
			print('{}: {} ({})'.format(char.initiative, char.name, char.dex_bonus))
		else:
			print('{}: {} ({}) - ROLL OFF={}'.format(char.initiative, char.name, char.dex_bonus, char.roll_off))
	print()

def print_combat(combat):
	for k, v in combat.rounds.items():
		print(k, v)
		
def create_combat(combatants, f):
	# get combat name
	if f:
		combat_name = f.readline().strip()
		print('Combat name: ', combat_name)
	else:
		combat_name = input('Name of combat: ')
	# create combat object
	combat = Combat(combat_name)
	# add combatants to combat object
	for combatant in combatants:
		combat.combatants.append(combatant)
	return combat

def round_order(combatants, combat=None, f=False):
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
			over = input('Combat over [y/n]: ')
		if over == 'y':
			combat.add_round(round_dict)
			break
		combat.add_round(round_dict)
		round += 1
	return combat

def tiebreaker(combatants):
	'''Args: Combatants is a list of all combatants as Character objects sorted by Character.initiative
	   TODO: reduce duplicate code
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
							m.roll_off = int(input('{} roll: '.format(m.name)))
					combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1] = sorted(combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1], key=lambda x:x.roll_off, reverse=True)
					print_initiative_order(combatants)
	return combatants	
	
def write_combat_to_file(combat):
	print('printing {} to file'.format(combat.name))
	# print(combat.rounds)
	# print(combat.combatants)
	filename = datetime.now().strftime('%Y%m%d_%H%M%S_{}.pickle'.format(combat.name.replace(' ','_')))
	directory = 'combats'
	path = directory + '/' + filename
	try:
		with open(path, 'wb') as f:
			# print(combat)
			pickle.dump(combat, f)
	except Exception as e:
		print('Exception: ', e)

def get_combat_file(return_file=False, date_time=()):
	# Get files from directory
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

def get_combat_details():
	'''
	TODO: Prompt if new or resuming old combat
	'''
	# input_combat_name = input('Name of combat: ').lower()
	
	file_info = get_combat_file() # [['20220725', '081517', 'battle of later that afternoon'],..]
	# Give options to select from 'num_battles_displayed' most recent battles
	num_battles_displayed = 3
	print('Select from the {} most recent battles:'.format(num_battles_displayed))
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
	for k, v in combat_selection_dict.items():
		print(str(k) + ') ', v)
	selection_input = int(input('\nSelect a combat by list number: '))
	print('You have selected: ' + combat_selection_dict[selection_input])
	combat_file = get_combat_file(True, file_selection_dict[selection_input])
	with open('combats/' + combat_file, 'rb') as f:
		return pickle.load(f)

def read_pickled_file():
	combat = get_combat_details()
	print(combat.rounds)

def resume_combat():
	# get combatants
	# get combat details
	combat = get_combat_details()
	combat = round_order(combat.combatants, combat)
	write_combat_to_file(combat)

def start_combat():
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters())
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	combatants = tiebreaker(combatants)
	combat = round_order(combatants)
	write_combat_to_file(combat)

def run():
	new_or_existing = input('Combat:\n1) [N]ew\n2) [E]xisting\n: ').lower()
	if new_or_existing == 'n' or new_or_existing == 'new' or new_or_existing == '1':
		start_combat()
	elif new_or_existing == 'e' or new_or_existing == 'existing' or new_or_existing == '2':
		resume_combat()

def main():
	run()
	
if __name__ == '__main__':
	main()
	
	# test_tiebreak()
	# test_combat()
	# resume_combat()
	# read_pickled_file()
	