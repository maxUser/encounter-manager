import csv
import sys
from random import randint

class Character:
	def __init__(self, name, initiative, pc, dex_bonus=0):
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

		
def player_characters():
	# dame_init = input('Dame Romaine initiative: ')
	# dennis_init = input('Dennis Le Menace initiative: ')
	# ronan_init = input('Ronan initiative: ')
	# pierre_init = input('Pierre initiative: ')
	
	#return [Character('Dame Romaine', dame_init), Character('Dennis Le Menace', dennis_init), Character('Ronan', ronan_init), Character('Pierre', pierre_init)]
	return [Character('Dame Romaine', 7, True, -2), Character('Dennis Le Menace', 7, True, 2), Character('Ronan', 21, True, 1), Character('Pierre', 21, True, 1)]
	
#f = open('test_combat.txt', 'r')
  
def nonplayer_characters():
	f = open('test_tiebreak.txt', 'r') 
	npc_name = ''
	npc_list = []
	while True:
		try:
			npc_name = f.readline().strip()
		except:
			npc_name = input('Monster name: ')
		if len(npc_name) < 2:
			break
		try:
			num_npc = int(f.readline().strip())
		except:
			num_npc = int(input('Number of ' + npc_name + 's: '))
		  
		try:
			dex_bonus = int(f.readline().strip())
		except:
			# get dex_bonus
			dex_bonus = get_dex_bonus(npc_name)
		
		if num_npc > 1:
			for i in range(num_npc):
				# add consecutive numbers after each npc name
				npc_multi = npc_name + str(i+1)
				npc_list.append(Character(npc_multi, get_npc_init(dex_bonus), False, dex_bonus))
		else:
			npc_list.append(Character(npc_name, get_npc_init(dex_bonus), False, dex_bonus))   
	
	return npc_list

def get_dex_bonus(npc_name):
	monster_file = open('monsters.csv', 'r')
	monsters = csv.reader(monster_file)
	
	monster_in_file = False
	dex_bonus = 0
	for monster_row in monsters:
		if monster_row[0] == npc_name.lower():
			monster_in_file = True
			return int(monster_row[1])
	return int(input(npc_name + ' dex bonus: '))        
	
def get_npc_init(dex_bonus):
	return int(randint(1,20) + dex_bonus)
 
def print_combatants(combatants):
	for char in combatants:
		print(str(char.initiative) + ': ' + char.name + '(' + str(char.dex_bonus) + ')')

def print_combat(combat):
	for k, v in combat.rounds.items():
		print(k, v)
		
def round_order(combatants):
	try:
		combat_name = f.readline().strip()
	except:
		combat_name = input('Name of combat: ')
	print('combat name: ', combat_name)
	combat = Combat(combat_name)
	round = 1
	round_dict = {}
	while True:
		round_dict[round] = {} # {1:{'Ronan': 'hit goblin for 2 dmg', 'Pierre'...}, 2:{}}
		print ('\-/-\-/-\-/-\-/-\-/-\\')
		print('ROUND ' + str(round))
		print ('/-\-/-\-/-\-/-\-/-\-/')
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
			print('over: ', over)
		except:
			over = input('Combat over [y/n]')
		if over == 'y':
			combat.add_round(round_dict)
			break
		combat.add_round(round_dict)
		round += 1
	combat.print_combat()

def tiebreaker(combatants):
	'''Args: Combatants is a list of all combatants as Character objects sorted by Character.initiative
	   TODO: reduce duplicate code
	'''
	tie_start_ind = 0
	tie_end_ind = 0
	print_combatants(combatants)
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
			# search through the tied initiative set looking for tied dex bonuses
			init_set = combatants[tie_start_ind:tie_end_ind+1]
			dex_bonus_tie_start_ind = 0
			dex_bonus_tie_end_ind = 0
			for j in range(init_set):
				print(j)
				dex_bonus_end_found = False
				if init_set[j].dex_bonus == init_set[j+1].dex_bonus and j == 0:
					# if it's the first element
					dex_bonus_tie_start_ind = j
				elif init_set[j].dex_bonus == init_set[j+1].dex_bonus and init_set[j].dex_bonus != init_set[j-1].dex_bonus:
					dex_bonus_tie_start_ind = j
				if init_set[j].dex_bonus != init_set[j+1].dex_bonus and init_set[j].dex_bonus == init_set[j-1].dex_bonus:
					dex_bonus_tie_end_ind = j
					dex_bonus_end_found = True
				elif init_set[j].dex_bonus == init_set[j-1].dex_bonus and j == len(init_set)-1:
					# if it's the last element
					dex_bonus_tie_end_ind = j
					dex_bonus_end_found = True
				if dex_bonus_end_found:
					# print('ROLL OFF at {}'.format(init_set[dex_bonus_tie_start_ind].dex_bonus))
					for m in init_set[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1]:
						if not m.pc:
							m.roll_off = int(randint(1,20))
							print('{} rolled {}'.format(m.name, m.roll_off))
						else:
							m.roll_off = int(input('{} roll: '.format(m.name)))
					combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1] = sorted(init_set[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1], key=lambda x:x.roll_off, reverse=True)
	print_combatants(combatants)
	sys.exit()
		
	
def main():
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters())
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	# 
	combatants = tiebreaker(combatants)
	
	#round_order(combatants)
	try:
		f.close()
	except:
		print()
	
if __name__ == '__main__':
	main()
	