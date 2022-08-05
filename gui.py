from msilib.schema import ListBox
from tkinter import *
from tkinter import ttk
from run_combat import display_combat_options, get_combat_based_on_selection
from Combat import Combat
from Character import Character

class CombatManager:

	def __init__(self, root):

		self.turnIndex = 0
		self.rowIndex = 0
		self.roundCount = 0
		self.currentRound = {}
		self.allCombatantLabels = []
		self.allActionTextboxes = []

		root.title("Encounter Manager")
		mainframe = ttk.Frame(root, padding="3 3 12 12")
		mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)

		ttk.Button(mainframe, text="New", command=lambda:self.test(mainframe)).grid(column=1, row=2, sticky=E)
		ttk.Button(mainframe, text="Existing", command=lambda:self.test(root, mainframe)).grid(column=3, row=2, sticky=W)

		ttk.Label(mainframe, text="Combat").grid(column=2, row=1, sticky=S)

		for child in mainframe.winfo_children(): 
			child.grid_configure(padx=5, pady=5)

	def test(self, root, mainframe):
		mainframe.destroy()
		existing = ttk.Frame(root, padding="3 3 12 12")
		existing.grid(column=0, row=0, sticky=(N, W, E, S))
		root.geometry("400x200")

		combat_selection_dict, file_selection_dict = display_combat_options(3, True)
		list_of_combats = [*combat_selection_dict.values()]
		longest_string = 0
		for combat in list_of_combats:
			if len(combat) > longest_string:
				longest_string = len(combat)
		# combat_selection_box = ttk.Combobox(existing, width=longest_string, value=list_of_combats)
		# combat_selection_box.grid(column=1, row=1, sticky=(N,E))
		listbox_choiced = StringVar(value=list_of_combats)
		combat_selection_box = Listbox(existing, width=longest_string, height=len(list_of_combats), listvariable=listbox_choiced)
		combat_selection_box.grid(column=1, row=1, sticky=(N,E))
		ttk.Button(existing, text="Select", command=lambda:self.select_existing_combat(combat_selection_box, file_selection_dict, root, existing)).grid(column=1, row=2, sticky=W)
	
	def displayPreviousRounds(self, roundNum, roundActions, listbox):
		listbox.insert('end', roundNum)
		listbox.insert('end', roundActions)
		
	def select_existing_combat(self, combat_selection_box, file_selection_dict, root, existing):
		root.geometry("1000x500")
		selection_index = combat_selection_box.curselection()[0] + 1
		combat = get_combat_based_on_selection(selection_index, file_selection_dict)
		existing.destroy()
		combatScreen = ttk.Frame(root, padding="3 3 12 12")
		combatScreen.grid(column=0, row=0, sticky=(N, W, E, S))

		ttk.Separator(combatScreen, orient=VERTICAL).grid(column=10, row=0, ipady=300, padx=10, pady=10, rowspan=20)
		ttk.Separator(combatScreen, orient=VERTICAL).grid(column=20, row=0, ipady=300, padx=10, pady=10, rowspan=20)
		
		# listbox and scrollbar
		prevRoundListbox = Listbox(combatScreen, width=35, height=27)
		prevRoundListbox.grid(column=0, row=1, rowspan=30, sticky=N, columnspan=6)
		xScrollbar = Scrollbar(combatScreen, orient=HORIZONTAL)
		xScrollbar.grid(row=15, column=0, columnspan=6, sticky=(N,E,W))
		prevRoundListbox.config(xscrollcommand=xScrollbar.set)
		xScrollbar.config(command=prevRoundListbox.xview)

		ttk.Label(combatScreen, text="Previous Rounds").grid(column=1, row=0, sticky=N, columnspan=6)
		rowCount = 1
		roundCount = 0
		# display previous rounds in left panel listbox
		for k, v in combat.rounds.items():
			if int(k) > roundCount:
				roundCount = int(k) + 1
			self.displayPreviousRounds(k, v, prevRoundListbox)
			rowCount+=2

		allInitOrderLabels = []

		# display initiative order on right panel
		ttk.Label(combatScreen, text='Initiative Order').grid(column=21, row=0, stick=N, columnspan=6)
		rowCount = 1
		for combatant in combat.combatants:
			initOrderLabel = ttk.Label(combatScreen, text=combatant)
			initOrderLabel.grid(column=21, row=rowCount, sticky=(N,W))
			allInitOrderLabels.append(initOrderLabel)
			rowCount+=1
		
		ttk.Label(combatScreen, text='Round ' + str(roundCount)).grid(column=11, row=0, stick=N, columnspan=3)
		ttk.Button(combatScreen, text='Prev', command=lambda:self.goToPreviousCombatant(combatScreen, combat)).grid(column=13, row=1, stick=E, padx=10)
		ttk.Button(combatScreen, text='Next', command=lambda:self.iterateCombatants(combatScreen, combat, prevRoundListbox)).grid(column=13, row=2, stick=E, padx=10)

	def goToPreviousCombatant(self, combatScreen, combat):
		print('hi')

	def iterateCombatants(self, combatScreen, combat, prevRoundListbox):
		'''Print the next combatant to list of combatants on screen. 
		'''
		combatantsList = combat.combatants
		# Printing the combatants and text boxes
		# first, move existing label/text boxes down
		currentCombatant = ''
		if self.allCombatantLabels:
			for existingCombatantLabel in self.allCombatantLabels:
				row = existingCombatantLabel.grid_info()['row']
				currentCombatant = existingCombatantLabel['text']
				if currentCombatant not in self.currentRound:
					self.currentRound[currentCombatant] = ''
				existingCombatantLabel.grid(column=11, row=row+1)
		if self.allActionTextboxes:
			for existingActionTextbox in self.allActionTextboxes:
				row = existingActionTextbox.grid_info()['row']
				self.currentRound[currentCombatant] = existingActionTextbox.get('1.0', 'end')[:-1]
				existingActionTextbox.grid(column=12, row=row+1)
				existingActionTextbox['state'] = 'disabled' # 'normal' to re-enable
				existingActionTextbox.config(background='#f0f0f0')

		# second, check if round over
		if self.turnIndex == len(combatantsList):
			print('end of turn')
			# update round label
			roundLabel = combatScreen.grid_slaves(column=11, row=0)[0]
			self.roundCount = int(roundLabel['text'][6:])
			newRoundCount = self.roundCount+1
			roundLabel.config(text='Round ' + str(newRoundCount))
			# add round to combat object
			combat.add_round(self.currentRound)
			# update previous rounds panel
			self.displayPreviousRounds(self.roundCount, self.currentRound, prevRoundListbox)
			self.currentRound.clear()
			self.turnIndex = 0
			# remove previous round label/boxes from middle panel

		
		# third, add new label/textbox
		newCombatantLabel = ttk.Label(combatScreen, text=combatantsList[self.turnIndex].name)
		self.allCombatantLabels.append(newCombatantLabel)
		self.allCombatantLabels[self.rowIndex].grid(column=11, row=1, sticky=(N,W))
		newActionTextbox = Text(combatScreen, width=25, height=2)
		self.allActionTextboxes.append(newActionTextbox)
		self.allActionTextboxes[self.rowIndex].grid(column=12, row=1, sticky=(N,W), rowspan=2)
		self.rowIndex += 1
		self.turnIndex += 1
		
root = Tk()
CombatManager(root)
root.mainloop()