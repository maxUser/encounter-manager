import csv
import sys
from random import randint

class Character:
    def __init__(self, name, initiative):
        self.name = name
        self.initiative = initiative
        
    def print_character(self):
        print(self.name, self.initiative)
        
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
    return [Character('Dame Romaine', 14), Character('Dennis Le Menace', 7), Character('Ronan', 21), Character('Pierre', 8)]
    
   
#f = open('test_combat.txt', 'r')   
def nonplayer_characters():
    
    npc_name = ''
    npc_list = []
    init = 0
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
                init = get_npc_init(dex_bonus)
                npc_list.append(Character(npc_multi, init))
        else:
            init = get_npc_init(dex_bonus)
            npc_list.append(Character(npc_name, init))   
    
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
    tie_exists = False
    for combatantX in combatants:
        for combatantY in combatants:
            if combatantX.initiative == combatantY.initiative and combatantX.name != combatantY.name:
                tie_exists = True
    print('tie: ', tie_exists)
    if tie_exists is True:
        print('tie')
    else:
        return combatants
    
def main():
    combatants = []
    combatants.extend(player_characters())
    combatants.extend(nonplayer_characters())
    combatants.sort(key=lambda x:x.initiative, reverse=True)
    print_combatants(combatants)
    combatants = tiebreaker(combatants)
    
    round_order(combatants)
    try:
        f.close()
    except:
        print()
    
if __name__ == '__main__':
    main()
    