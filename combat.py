class Character:
    def __init__(self, name, initiative):
        self.name = name
        self.initiative = initiative
        
class Combat:
    def __init__(self, name):
        self.name = name
        self.rounds = {}
    def add_round(self, round):
        self.rounds.update(round)
    def print_combat(self):
        print(self.name)
        #print(self.rounds)
        for k, v in self.rounds.items():
            print(k, v)

        
def player_characters():
    #return {'Dame Romaine':14, 'Dennis Le Menace':7, 'Ronan':21, 'Pierre':8}
    return [Character('Dame Romaine', 14), Character('Dennis Le Menace', 7), Character('Ronan', 21), Character('Pierre', 8)]
    
   
f = open('test_combat.txt', 'r')   
def nonplayer_characters():
    
    npc_name = ''
    npc_list = []
    while True:
        try:
            npc_name = f.readline().strip()
        except:
            npc_name = input('NPC Name: ')
        if len(npc_name) < 2:
            break
        try:
            num_npc = int(f.readline().strip())
        except:
            num_npc = int(input('Number of ' + npc_name + 's: '))
        if num_npc > 1:
            for i in range(num_npc):
                npc_multi = npc_name + str(i+1)
                try:
                    init = int(f.readline().strip())
                except:
                    init = int(input(npc_multi + ' initiative: '))
                npc_list.append(Character(npc_multi, init))
        else:
            init = int(input(npc_name + ' initiative: '))
            npc_list.append(Character(npc_name, init))   
    return npc_list
    
    
def print_combatants(combatants):
    for char in combatants:
        print(char.name + ': ' + str(char.initiative))

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
        try:
            over = f.readline().strip()
            print('over: ', over)
        except:
            over = input('Combat over [y/n]')
        print('ROUND ' + str(round) + ' END')
        if over == 'y':
            combat.add_round(round_dict)
            break
        combat.add_round(round_dict)
        round += 1
    combat.print_combat()
def main():
    combatants = []
    combatants.extend(player_characters())
    combatants.extend(nonplayer_characters())
    combatants.sort(key=lambda x:x.initiative, reverse=True)
    print_combatants(combatants)
    round_order(combatants)
    try:
        f.close()
    except:
        print()
    
if __name__ == '__main__':
    main()
    