class Combat:
	'''
	A class used to store combat encounter data

	Attributes
	----------
	name : str
		A string storing the Combat's name
	rounds : dictionary
		A dictionary storing the actions in each round of Combat (key=round number, value=dictionary with each entry as {combatant.name:action})
	combatants : Character
		A list of Character objects participating in the Combat

	Functions
	---------
	add_round(round)
		Adds the given round to the Combat's rounds dictionary
	print_combat()
		Prints a Combat's rounds in a human readable format
	'''
	
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