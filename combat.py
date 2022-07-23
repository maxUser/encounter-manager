import csv
import json

from datetime import datetime
from random import randint


'''
	TODO: input error checking
	TODO: save combat in progress and resume where it left off
	TODO: ask to add new monsters to monsters.csv
'''

class Character:
	def __init__(self, name, initiative, dex_bonus=0, pc=True):
		self.name = name
		self.initiative = initiative
		self.dex_bonus = dex_bonus
		self.pc = pc
		self.roll_off = 0
		
	def print_character(self):
		print(self.name, self.initiative, self.dex_bonus)
		
	def __str__(self):
		return self.name
		
class Combat:
	def __init__(self, name):
		self.name = name
		self.rounds = {}
	def add_round(self, round):
		self.rounds.update(round)
	def print_combat(self):
		print(self.name)
		for k, v in self.rounds.items():
			print(k, v)
	def __str__(self):
		return self.name
		
def test_combat():
	f = open('test_combat.txt', 'r')
	npc_name = f.readline().strip()
	dex_bonus = f.readline().strip()
	num_npc = int(f.readline().strip())

def player_characters():
	pc_list = ['Dennis Le Menace', 'Pierre', 'Ronan', 'Dame Romaine']
	pcs = []
	for pc in pc_list:
		# pc_init = int(randint(1,20))
		pc_init = get_quantity_input('{} initiative: '.format(pc))
		print(pc, pc_init)
		pc_dex_bonus = get_dex_bonus(pc)
		pcs.append(Character(pc, pc_init, pc_dex_bonus))
	return pcs

def get_quantity_input(something):
	while True:
		try:
			return int(input(something))
		except ValueError:
			print('Invalid input, please enter a number.')

def nonplayer_characters():
	#f = open('test_tiebreak.txt', 'r') 
	npc_name = ''
	npc_list = []
	while True:
		npc_name = input('Monster name: ')
		if len(npc_name) < 2:
			print()
			break

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
		
def round_order(combatants):
	try:
		combat_name = f.readline().strip()
	except:
		combat_name = input('Name of combat: ')
	combat = Combat(combat_name)
	round = 1
	round_dict = {}
	while True:
		round_dict[round] = {} # {1:{'Ronan': 'hit goblin for 2 dmg', 'Pierre'...}, 2:{}}
		print('========================')
		print('========================')
		print('====== ROUND {} ========'.format(str(round)))
		print('========================')
		print('========================')
		for i in range(len(combatants)):
			print(combatants[i].name + '\'s turn')
			try:
				round_dict[round][combatants[i].name] = f.readline().strip()
				print('action: ', round_dict[round][combatants[i].name])
			except:
				round_dict[round][combatants[i].name] = input(': ')
		print('ROUND ' + str(round) + ' END')
		try:
			over = f.readline().strip()
			print('Combat over [y/n]: ', over)
		except:
			over = input('Combat over [y/n]: ')
		if over == 'y':
			combat.add_round(round_dict)
			break
		combat.add_round(round_dict)
		round += 1
	# combat.print_combat()
	return combat

def tiebreaker(combatants):
	'''Args: Combatants is a list of all combatants as Character objects sorted by Character.initiative
	   TODO: reduce duplicate code
	   TODO: ability to manually rearrange initiative order
	'''
	tie_start_ind = 0
	tie_end_ind = 0
	for i in range(len(combatants)-1):
		# get start and end indices of tied combatants in list
		# sort each tie set by dex bonus
		end_found = False
		if combatants[i].initiative == combatants[i+1].initiative and i == 0:
			# if it's the first element
			tie_start_ind = i
		elif combatants[i].initiative == combatants[i+1].initiative and combatants[i].initiative != combatants[i-1].initiative:
			tie_start_ind = i
		if combatants[i].initiative != combatants[i+1].initiative and combatants[i].initiative == combatants[i-1].initiative:
			tie_end_ind = i
			end_found = True
		elif combatants[i].initiative == combatants[i-1].initiative and i == len(combatants)-1:
			# if it's the last element
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
				if combatants[j].dex_bonus == combatants[j+1].dex_bonus and j == tie_start_ind:
					# if it's the first element
					dex_bonus_tie_start_ind = j
				elif combatants[j].dex_bonus == combatants[j+1].dex_bonus and combatants[j].dex_bonus != combatants[j-1].dex_bonus:
					dex_bonus_tie_start_ind = j
				# else:
				# 	print(combatants[j].name, 'A')
				if combatants[j].dex_bonus != combatants[j+1].dex_bonus and combatants[j].dex_bonus == combatants[j-1].dex_bonus and combatants[j].initiative == combatants[j-1].initiative:
					dex_bonus_tie_end_ind = j
					dex_bonus_end_found = True
				elif combatants[j].dex_bonus == combatants[j-1].dex_bonus and j == tie_end_ind:
					# if it's the last element
					# print('Last ele/j: {}/{}'.format(combatants[j], j))
					dex_bonus_tie_end_ind = j
					dex_bonus_end_found = True
				# else:
				# 	print(combatants[j].name, 'B')
				if dex_bonus_end_found:
					#print('DEX BONUS tie_start:end {}:{}'.format(dex_bonus_tie_start_ind, dex_bonus_tie_end_ind))
					print('ROLL OFF at {}'.format(combatants[dex_bonus_tie_start_ind].dex_bonus))
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
	filename = datetime.now().strftime('%Y%m%d_%H%M%S_{}.json'.format(combat.name.replace(' ','_')))
	directory = 'combats'
	path = directory + '/' + filename
	with open(path, 'w') as outfile:
		json.dump(combat.rounds, outfile)

def main():
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters())
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	combatants = tiebreaker(combatants)
	# print_initiative_order(combatants)
	combat = round_order(combatants)
	# write_combat_to_file(combat)
	try:
		f.close()
	except:
		print()
	
if __name__ == '__main__':
	main()
	