class Character:
	'''
	A class used to represent participants in a combat encounter

	Attributes
	----------
	name : str
		A string storing the Character's name
	initiative : int
		An integer storing the Character's initiative
	dex_bonus : int
		An integer storing the Character's dexterity bonus
	pc : boolean
		A boolean tracking whether a Character is a PC or an NPC (True=PC, False=NPC, default True)
	roll_off : int
		An integer storing the Character's roll off value in the case of a initiative and dexterity bonus tie

	Functions
	---------
	print_character()
		Prints a Character's attributes in a human readable format
	'''

	def __init__(self, name, initiative, dex_bonus=0, pc=True):
		self.name = name
		self.initiative = initiative
		self.dex_bonus = dex_bonus
		self.pc = pc
		self.roll_off = 0	
	def print_character(self):
		if self.roll_off > 0:
			print('{}\n\tinitiative: {} [{}]'.format(self.name, self.initiative, self.dex_bonus))
		else:
			print('{}\n\tinitiative: {} [{}] - ROLL OFF={}'.format(self.name, self.initiative, self.dex_bonus, self.roll_off))