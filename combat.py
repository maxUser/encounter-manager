import csv
import sys
from random import randint

class Character:
	def __init__(self, name, initiative, dex_bonus=0):
		self.name = name
		self.initiative = initiative
		self.dex_bonus = dex_bonus
		
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
	return [Character('Dame Romaine', 7, -2), Character('Dennis Le Menace', 7, 2), Character('Ronan', 21, 1), Character('Pierre', 21, 1)]
	
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
				npc_list.append(Character(npc_multi, get_npc_init(dex_bonus), dex_bonus))
		else:
			npc_list.append(Character(npc_name, get_npc_init(dex_bonus), dex_bonus))   
	
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
		print(str(char.initiative) + ': ' + char.name)

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
	# Args: Combatants is a list of all combatants as Character objects sorted by Character.initiative
	tie_exists = False
	for combatantX in combatants:
		# Test if tie exists
		for combatantY in combatants:
			if combatantX.initiative == combatantY.initiative and combatantX.name != combatantY.name:
				tie_exists = True
	print('tie: ', tie_exists)
	if tie_exists is True:
		# Get the value of the tied initiative scores and the characters with those scores
		tied_combatants = {} # {17: [('Pierre', 0), ('Ronan', 1)], 4: [('Dame Romaine', 2), ('Dennis', 3)]}
		for combatantX in combatants:
			for combatantY in combatants:
				if combatantX.initiative == combatantY.initiative:
					# Get all tied initiative scores, store them as keys
					tied_combatants[combatantX.initiative] = []
		for combatant in combatants:
			if combatant.initiative in tied_combatants:
				# Add combatants as values (combatant, index) to respective initiative key
				tied_combatants[combatant.initiative].append([combatant, combatants.index(combatant)])
		# for k, v in tied_combatants.items():
		# 	print()
		# 	print('binit: ', k)
		# 	for tup in v:
		# 		tup[0].print_character()
		# 		print('bind: ', tup[1])
		for init in tied_combatants.keys():
			# compare the dex bonus of each tied set of characters
			# swap them in the combat order depending on their dex bonuses
			# bubble sort because why not
			n = len(tied_combatants[init])
			for i in range(n-1, 0, -1):
				for j in range(i):
					if tied_combatants[init][j][0].dex_bonus < tied_combatants[init][j+1][0].dex_bonus:
						temp = tied_combatants[init][j][1]
						tied_combatants[init][j][1] = tied_combatants[init][j+1][1]
						print('less than: ', tied_combatants[init][j][0].print_character())
						print('greater than: ', tied_combatants[init][j+1][0].print_character())
						tied_combatants[init][j+1][1] = temp

		# Put the characters back into the list according to their new indices
		for init in tied_combatants.keys():
			for i in range(len(tied_combatants[init])):
				combatants[tied_combatants[init][i][1]] = tied_combatants[init][i][0]
		print()
		print()
			
		for k in combatants:
			k.print_character()
	else:
		return combatants
	
def main():
	combatants = []
	combatants.extend(player_characters())
	combatants.extend(nonplayer_characters())
	combatants.sort(key=lambda x:x.initiative, reverse=True)
	print_combatants(combatants)
	combatants = tiebreaker(combatants)
	
	#round_order(combatants)
	try:
		f.close()
	except:
		print()
	
if __name__ == '__main__':
	main()
	