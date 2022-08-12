
from tkinter import *
import tkinter.font as tkFont
from ttkbootstrap.constants import *
import ttkbootstrap as ttk

from run_combat import display_combat_options, get_combat_based_on_selection, write_combat_to_file
# required for loading existing files
from Combat import Combat
from Character import Character

class CombatManager:

	def __init__(self, root):

		self.turnIndex = 0
		self.rowIndex = 0
		self.roundCount = 0
		self.roundDict = {}
		self.currentRound = {}
		self.allCombatantLabels = []
		self.allActionTextboxes = []
		self.roundLabelList = []
		self.allButtonsDict = {}
		self.LEFT_PANE_COLUMN = 0
		self.MIDDLE_PANE_COLUMN = 7
		self.RIGHT_PANE_COLUMN = 19
		self.LEFT_SEPARATOR_COLUMN = 6
		self.RIGHT_SEPARATOR_COLUMN = 18
		self.PANE_LABEL_ROW = 0
		self.LISTBOX_SCROLLBAR_ROW = 1
		self.LISTBOX_ROW = self.LISTBOX_SCROLLBAR_ROW + 1
		self.LISTBOX_HEIGHT = 27
		self.PREV_BTN_COLUMN = 8
		self.NEXT_BTN_COLUMN = 12
		self.COMBAT_OVER_BTN_COLUMN = 14
		self.ITERATE_BTN_ROW = 1
		self.primaryTitleFont = tkFont.Font(family='Bahnschrift SemiBold', size=20)
		self.secondaryTitleFont = tkFont.Font(family='Bahnschrift SemiBold', size=14)
		self.tertiaryTitleFont = tkFont.Font(family='Bahnschrift Light Condensed', size=10)
		
		root.title('Encounter Manager')
		mainMenu = ttk.Frame(root, padding='3 3 12 12')
		mainMenu.grid(column=0, row=0, sticky=(N, W, E, S))
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		root.geometry('225x100')

		ttk.Button(mainMenu, text='New', bootstyle=ttk.SUCCESS, command=lambda:self.goToMainMenu(root)).grid(column=2, row=2, sticky=S)
		ttk.Button(mainMenu, text='Existing', command=lambda:self.combatSelectionView(root, mainMenu)).grid(column=3, row=2, sticky=S)

		
		ttk.Label(mainMenu, text='Combat', font=self.primaryTitleFont).grid(column=2, row=0, sticky=S, columnspan=4)
		# print([x for x in tkFont.families() if 'Bahnschrift' in x])

		for child in mainMenu.winfo_children():
			child.grid_configure(padx=5, pady=5)

	def combatSelectionView(self, root, mainMenu):
		mainMenu.destroy()
		existing = ttk.Frame(root, padding='3 3 12 12')
		existing.grid(column=0, row=0, sticky=(N, W, E, S))
		root.geometry('400x200')

		combat_selection_dict, file_selection_dict = display_combat_options(5, True)
		list_of_combats = [*combat_selection_dict.values()]
		longest_string = 0
		for combat in list_of_combats:
			if len(combat) > longest_string:
				longest_string = len(combat)
		
		ttk.Label(existing, text='Select A Combat', font=self.primaryTitleFont).grid(column=0, row=0, sticky=S, columnspan=4)
		listbox_choiced = StringVar(value=list_of_combats)
		combat_selection_box = Listbox(existing, width=longest_string, height=len(list_of_combats), listvariable=listbox_choiced)
		combat_selection_box.grid(column=1, row=1, sticky=(N,E))
		ttk.Button(existing, text='Select', command=lambda:self.existingCombatView(combat_selection_box, file_selection_dict, root, existing)).grid(column=1, row=2, sticky=W, pady=5)
	
	def displayPreviousRounds(self, roundNum, roundActions, listbox):
		listbox.insert('end', roundNum)
		listbox.insert('end', roundActions)
		
	def existingCombatView(self, combat_selection_box, file_selection_dict, root, existing):
		root.geometry('1000x500')
		selection_index = combat_selection_box.curselection()[0] + 1
		combat = get_combat_based_on_selection(selection_index, file_selection_dict)
		existing.destroy()
		combatScreen = ttk.Frame(root, padding='3 3 12 12')
		combatScreen.grid(column=0, row=0, sticky=(N, W, E, S))

		ttk.Separator(combatScreen, orient=VERTICAL).grid(column=self.LEFT_SEPARATOR_COLUMN, row=self.PANE_LABEL_ROW, ipady=500, padx=15, rowspan=50)
		ttk.Separator(combatScreen, orient=VERTICAL).grid(column=self.RIGHT_SEPARATOR_COLUMN, row=self.PANE_LABEL_ROW, ipady=500, padx=15, rowspan=50)
		
		'''
			LEFT: listbox and scrollbar
		'''
		ttk.Label(combatScreen, text='Previous Rounds', font=self.secondaryTitleFont).grid(column=self.LEFT_PANE_COLUMN, row=self.PANE_LABEL_ROW, sticky=N, columnspan=6)
		prevRoundListbox = Listbox(combatScreen, width=35, height=self.LISTBOX_HEIGHT)
		prevRoundListbox.grid(column=self.LEFT_PANE_COLUMN, row=self.LISTBOX_ROW, rowspan=100, sticky=N, columnspan=6)
		xScrollbar = Scrollbar(combatScreen, orient=HORIZONTAL)
		xScrollbar.grid(row=self.LISTBOX_SCROLLBAR_ROW, column=0, columnspan=6, sticky=(N,E,W))
		prevRoundListbox.config(xscrollcommand=xScrollbar.set)
		xScrollbar.config(command=prevRoundListbox.xview)

		# display previous rounds in left panel listbox
		rowCount = 1
		for k, v in combat.rounds.items():
			if int(k) > self.roundCount:
				self.roundCount = int(k) + 1
			self.displayPreviousRounds(k, v, prevRoundListbox)
			rowCount+=2

		'''
			RIGHT: listbox/initiative order
		'''
		ttk.Label(combatScreen, text='Initiative Order', font=self.secondaryTitleFont).grid(column=self.RIGHT_PANE_COLUMN, row=self.PANE_LABEL_ROW, sticky=N, columnspan=6)
		initOrderListbox = Listbox(combatScreen, width=45, height=self.LISTBOX_HEIGHT)
		initOrderListbox.grid(column=self.RIGHT_PANE_COLUMN, row=self.LISTBOX_ROW-1, rowspan=100, sticky=N, columnspan=6)
		for combatant in combat.combatants:
			initOrderListbox.insert('end', combatant)	

		'''
			MIDDLE: ROUND LABEL
		'''
		roundLabel = ttk.Label(combatScreen, text='Round ' + str(self.roundCount), font=self.secondaryTitleFont)
		roundLabel.grid(column=self.MIDDLE_PANE_COLUMN, row=self.PANE_LABEL_ROW, sticky=N, columnspan=10)
		self.roundLabelList.append(roundLabel)

		'''
			MIDDLE: COMBAT BUTTONS
		'''
		prevBtn = ttk.Button(combatScreen, state='disabled', text='Prev', command=lambda:self.goToPreviousCombatant())
		prevBtn.grid(column=self.PREV_BTN_COLUMN, row=self.ITERATE_BTN_ROW, sticky=E, ipadx=2, padx=5)
		self.allButtonsDict['prevBtn'] = prevBtn
		nextBtn = ttk.Button(combatScreen, text='Next', command=lambda:self.iterateCombatants(combatScreen, combat, prevRoundListbox))
		nextBtn.grid(column=self.NEXT_BTN_COLUMN, row=self.ITERATE_BTN_ROW, ipadx=2, padx=5)
		self.allButtonsDict['nextBtn'] = nextBtn
		combatOverBtn = ttk.Button(combatScreen, text='End Combat', bootstyle=ttk.DANGER, command=lambda:self.combatOver(combat))
		combatOverBtn.grid(column=self.COMBAT_OVER_BTN_COLUMN, row=self.ITERATE_BTN_ROW, sticky=W, ipadx=2, padx=5)
		self.allButtonsDict['combatOverBtn'] = combatOverBtn
		# ttk.Button(combatScreen, text='Main', command=lambda:self.goToMainMenu(root)).grid(column=23, row=10, sticky=(S,E), padx=10, columnspan=6)

	def combatOver(self, combat):
		write_combat_to_file(combat)
		print('combat over')

	def goToMainMenu(self, root):
		self.__init__(root)

	def goToPreviousCombatant(self):
		if self.turnIndex <= 2:
			self.allButtonsDict['prevBtn']['state'] = 'disabled'
			# self.allButtonsDict['prevBtn'].configure({"disabledbackground": "red"})
		if self.allCombatantLabels:
			# remove current combatant label/text box
			self.allCombatantLabels[-1].destroy()
			self.allActionTextboxes[-1].destroy()
			del self.allCombatantLabels[-1]
			del self.allActionTextboxes[-1]
			# move previous combatants up one index
			for existingCombatantLabel in self.allCombatantLabels:
				row = existingCombatantLabel.grid_info()['row']
				existingCombatantLabel.grid(row=row-2)
			for existingActionTextbox in self.allActionTextboxes:
				row = existingActionTextbox.grid_info()['row']
				existingActionTextbox.grid(row=row-2)
				self.allActionTextboxes[-1]['state'] = 'normal' # 'normal' to re-enable
				self.allActionTextboxes[-1].config(background='white')

			self.rowIndex -= 1
			self.turnIndex -= 1

	def iterateCombatants(self, combatScreen, combat, prevRoundListbox):
		'''Print the next combatant to list of combatants on screen. 
		'''

		combatantsList = combat.combatants
		if self.turnIndex > 0:
			self.allButtonsDict['prevBtn']['state'] = 'normal'

		if self.turnIndex == len(combatantsList):
			# remove previous round label/boxes from middle panel
			for existingCombatantLabel in self.allCombatantLabels:
				existingCombatantLabel.grid_remove()
			for existingActionTextbox in self.allActionTextboxes:
				existingActionTextbox.grid_remove()
			self.allCombatantLabels.clear()
			self.allActionTextboxes.clear()
		# Printing the combatants and text boxes
		# first, move existing label/text boxes/buttons down
		currentCombatant = ''
		if self.allCombatantLabels:
			for existingCombatantLabel in self.allCombatantLabels:
				row = existingCombatantLabel.grid_info()['row']
				currentCombatant = existingCombatantLabel['text']
				if currentCombatant not in self.currentRound:
					self.currentRound[currentCombatant] = ''
				existingCombatantLabel.grid(column=self.MIDDLE_PANE_COLUMN, row=row+2, sticky=W, rowspan=2, columnspan=2)

		if self.allActionTextboxes:
			for existingActionTextbox in self.allActionTextboxes:
				row = existingActionTextbox.grid_info()['row']
				# get action of currentCombatant
				self.currentRound[currentCombatant] = existingActionTextbox.get('1.0', 'end')[:-1]
				# print(combat.rounds[self.currentRound])
				if self.roundCount not in combat.rounds:
					combat.rounds.update({self.roundCount:{}})
				# update combat object
				combat.rounds[self.roundCount].update(self.currentRound)
				existingActionTextbox.grid(column=self.MIDDLE_PANE_COLUMN+2, row=row+2, sticky=E, rowspan=2, columnspan=8)
				existingActionTextbox['state'] = 'disabled' # 'normal' to re-enable
				existingActionTextbox.config(background='#f0f0f0')
		# second, check if round over
		if self.turnIndex == len(combatantsList):
			# update previous rounds panel
			self.displayPreviousRounds(self.roundCount, self.currentRound, prevRoundListbox)
			# update round label
			self.roundCount+=1
			self.roundLabelList[0].config(text='Round ' + str(self.roundCount))
			# reset some variables
			self.turnIndex = 0
			self.currentRound = {}

		# third, add new label/textbox
		newCombatantLabel = ttk.Label(combatScreen, text=combatantsList[self.turnIndex].name, font=self.tertiaryTitleFont)
		newCombatantLabel.grid(column=self.MIDDLE_PANE_COLUMN, row=2, sticky=W, rowspan=2, columnspan=2)
		self.allCombatantLabels.append(newCombatantLabel)
		newActionTextbox = Text(combatScreen, width=25, height=2)
		newActionTextbox.grid(column=self.MIDDLE_PANE_COLUMN+2, row=2, sticky=E, rowspan=2, columnspan=8)
		self.allActionTextboxes.append(newActionTextbox)
		newActionTextbox.focus_set()

		self.rowIndex += 1
		self.turnIndex += 1
		
root = Tk()
CombatManager(root)
root.mainloop()