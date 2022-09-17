from tkinter import *
import tkinter.font as tkFont
from ttkbootstrap.constants import *
import ttkbootstrap as ttk

import csv

from run_combat import display_combat_options, get_combat_based_on_selection, write_combat_to_file, get_npc_init, tiebreaker
# required for loading existing files
from Combat import Combat
from Character import Character

# CONTINUING MOST RECNET COMBAT next round won't start

class CombatManager:

	def __init__(self, root):
		self.turnIndex = 0
		self.rowIndex = 0
		self.roundCount = 0
		self.nextCombatantInd = 999
		self.roundDict = {}
		self.currentRound = {}
		self.allCombatantLabels = []
		self.allActionTextboxes = []
		self.roundLabelList = []
		self.allButtonsDict = {}
		self.selectedNPCs = []
		self.selectedPCs = [Character('dame romaine', -2) , Character('ronan', 1), Character('pierre', 1), Character('dennis le menace', 2)]
		self.unselectedPCs = []
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
		self.tertiaryTitleFont = tkFont.Font(family='Bahnschrift Light Condensed', size=11)
		
		root.title('Combat Manager')
		mainMenu = ttk.Frame(root, padding='3 3 12 12')
		mainMenu.grid(column=0, row=0, sticky=(N, W, E, S))
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		root.geometry('275x125')

		ttk.Label(mainMenu, text='Combat', font=self.primaryTitleFont).grid(column=0, row=0, sticky=N, columnspan=4)

		ttk.Button(mainMenu, text='New', bootstyle=ttk.PRIMARY, command=lambda:self.npcSelectionView()).grid(column=0, row=1, sticky=S)
		ttk.Button(mainMenu, text='Existing', bootstyle=ttk.SECONDARY, command=lambda:self.combatSelectionView(root, mainMenu)).grid(column=2, row=1, sticky=S)
		# print([x for x in tkFont.families() if 'Bahnschrift' in x])
		for child in mainMenu.winfo_children():
			child.grid_configure(padx=5, pady=5)

	def createCharacterView(self):
		characterCreationView = ttk.Frame(root, padding='3 3 12 12')
		characterCreationView.grid(column=0, row=0, sticky=(N, W, E, S))
		root.geometry('400x155')
		root.title('Combat Manager - Character Creation')

		ttk.Label(characterCreationView, text='Create New Character', font=self.secondaryTitleFont).grid(column=self.LEFT_PANE_COLUMN+1, row=0, sticky=(N,E,W), columnspan=4)
		ttk.Label(characterCreationView, text='Name', font=self.tertiaryTitleFont).grid(column=self.LEFT_PANE_COLUMN, row=1, sticky=(N,E), pady=(10,0))
		nameStr = StringVar()
		nameEntry = Entry(characterCreationView, textvariable=nameStr, width=30)
		nameEntry.grid(column=self.LEFT_PANE_COLUMN+1, row=1, sticky=N, padx=5, pady=(10,0))
		ttk.Label(characterCreationView, text='Dex bonus', font=self.tertiaryTitleFont).grid(column=self.LEFT_PANE_COLUMN, row=2, sticky=(N,E), pady=5)
		dexStr = StringVar()
		dexEntry = Entry(characterCreationView, textvariable=dexStr, width=5)
		dexEntry.grid(column=self.LEFT_PANE_COLUMN+1, row=2, sticky=(N,W), pady=5, padx=5)
		ttk.Label(characterCreationView, text='PC/NPC', font=self.tertiaryTitleFont).grid(column=self.LEFT_PANE_COLUMN, row=3, sticky=(N,E), pady=5)
		pcNpcStr = StringVar()
		optionList = ('PC', 'NPC')
		pcNpcDropdown = OptionMenu(characterCreationView, pcNpcStr, *optionList)
		pcNpcDropdown.config(bg='white')
		pcNpcDropdown.config(activebackground='light grey')
		pcNpcDropdown.config(fg='black')
		pcNpcDropdown.grid(column=self.LEFT_PANE_COLUMN+1, row=3, sticky=(N,W), pady=5, padx=5)

		newCharacter = [nameEntry, dexEntry, pcNpcStr]

		ttk.Button(characterCreationView, bootstyle=ttk.SUCCESS, text='Save', command=lambda:self.addNewCharacterToFile(newCharacter)).grid(column=2, row=1, sticky=W, padx=40, pady=(10,0))
		ttk.Button(characterCreationView, bootstyle=ttk.DANGER, text='Cancel', command=lambda:self.npcSelectionView()).grid(column=2, row=2, sticky=W, padx=40, pady=(5,0))

	def addNewCharacterToFile(self, newCharacter):
		characterAttributes = []
		for w in newCharacter:
			characterAttributes.append(w.get().lower())
		if characterAttributes[0]:
			with open('monsters.csv', 'a', newline='') as csvfile:
				csv_writer = csv.writer(csvfile)
				csv_writer.writerow(characterAttributes)
		self.npcSelectionView()

	def pcSelectionView(self):
		pcSelectionView = ttk.Frame(root, padding='3 3 12 12')
		pcSelectionView.grid(column=0, row=0, sticky=(N, W, E, S))
		root.geometry('610x400')
		root.title('Combat Manager - PC Selection')
		
		'''
			MIDDLE: selected pc listbox, main menu button
		'''
		ttk.Label(pcSelectionView, text='Selected', font=self.secondaryTitleFont).grid(column=self.MIDDLE_PANE_COLUMN, row=1, sticky=(N,E,W), columnspan=6)
		selectedPCsListbox = Listbox(pcSelectionView, width=35, height=self.LISTBOX_HEIGHT)
		selectedPCsListbox.grid(column=self.MIDDLE_PANE_COLUMN, row=2, rowspan=100, sticky=N, columnspan=6)
		if self.selectedPCs:
			for pc in self.selectedPCs:
				selectedPCsListbox.insert(0, self.capitalizeName(pc.name))
		'''
			LEFT: unselected PCs listbox
		'''
		ttk.Label(pcSelectionView, text='Available', font=self.secondaryTitleFont).grid(column=self.LEFT_PANE_COLUMN, row=1, sticky=(N,E,W), columnspan=6)
		availableListbox = Listbox(pcSelectionView, width=35, height=self.LISTBOX_HEIGHT)
		availableListbox.grid(column=self.LEFT_PANE_COLUMN, row=2, rowspan=100, sticky=N, columnspan=6)
		
		with open('monsters.csv', newline='') as monsterFile:
			monsterReader = csv.reader(monsterFile, delimiter=',')
			for row in monsterReader:
				if row[2] == 'pc' and row[0] not in [x.name.lower() for x in self.selectedPCs]:
					pc = Character(row[0], row[1])
					self.unselectedPCs.append(pc)
					self.fillListbox([pc.name], availableListbox)
		self.unselectedPCs.sort(key=lambda x:x.name, reverse=True)
		# self.fillListbox([x.name for x in self.unselectedPCs], availableListbox)

		'''
			LEFT SEPARATOR: add/remove buttons
		'''
		ttk.Button(pcSelectionView, text='Add', bootstyle=ttk.SUCCESS, command=lambda:self.addSelectedPC(selectedPCsListbox, availableListbox)).grid(column=self.LEFT_SEPARATOR_COLUMN, row=10, sticky=S, padx=10, rowspan=20)
		ttk.Button(pcSelectionView, text='Remove', bootstyle=ttk.DANGER, command=lambda:self.removeSelectedPC(selectedPCsListbox, availableListbox)).grid(column=self.LEFT_SEPARATOR_COLUMN, row=20, sticky=S, padx=10, rowspan=20)

		'''
			RIGHT SEPARATOR: main menu/continue button
		'''
		ttk.Button(pcSelectionView, text='Back', bootstyle=ttk.DARK, command=lambda:self.npcSelectionView()).grid(column=self.RIGHT_SEPARATOR_COLUMN, row=8, sticky=N, padx=10, rowspan=20)
		ttk.Button(pcSelectionView, text='Continue', bootstyle=ttk.PRIMARY, command=lambda:self.npcSelectionView()).grid(column=self.RIGHT_SEPARATOR_COLUMN, row=10, sticky=S, padx=10, rowspan=20)

	def npcSelectionView(self):
		npcSelectionView = ttk.Frame(root, padding='3 3 12 12')
		npcSelectionView.grid(column=0, row=0, sticky=(N, W, E, S))
		root.geometry('610x500')
		root.title('Combat Manager - NPC Selection')

		'''
			LEFT: monster listbox and search bar
		'''
		monsterListbox = Listbox(npcSelectionView, width=35, height=self.LISTBOX_HEIGHT)
		monsterListbox.grid(column=self.LEFT_PANE_COLUMN, row=self.LISTBOX_ROW, rowspan=100, sticky=N, columnspan=6)
		NPCList = []
		with open('monsters.csv', newline='') as monsterFile:
			monsterReader = csv.reader(monsterFile, delimiter=',')
			for row in monsterReader:
				if row[2] == 'npc':
					NPCList.append(row[0])
		NPCList.sort()
		self.fillListbox(NPCList, monsterListbox)
		search_str = StringVar()
		searchBar = Entry(npcSelectionView, textvariable=search_str, width=30)
		searchBar.grid(column=self.LEFT_PANE_COLUMN, row=0, sticky=S, columnspan=6, pady=10)
		searchBar.bind('<Return>', lambda event, a=monsterListbox, b=NPCList, c=search_str: self.listboxSearch(a, b, c))

		'''
			LEFT SEPARATOR: add/remove buttons
		'''
		ttk.Button(npcSelectionView, text='Add', bootstyle=ttk.SUCCESS, command=lambda:self.addSelectedNPC(monsterListbox, selectedMonsterListbox, NPCList)).grid(column=self.LEFT_SEPARATOR_COLUMN, row=10, sticky=S, padx=10, rowspan=20)
		ttk.Button(npcSelectionView, text='Remove', bootstyle=ttk.DANGER, command=lambda:self.removeSelectedNPC(selectedMonsterListbox, NPCList)).grid(column=self.LEFT_SEPARATOR_COLUMN, row=20, sticky=S, padx=10, rowspan=20)

		'''
			MIDDLE: selected monster listbox, create button, PCs button, main menu button
		'''
		ttk.Button(npcSelectionView, text='Create', bootstyle=ttk.SUCCESS, command=lambda:self.createCharacterView()).grid(column=self.MIDDLE_PANE_COLUMN, row=0, sticky=N, padx=10, columnspan=2)
		ttk.Button(npcSelectionView, text='PCs', bootstyle=ttk.WARNING, command=lambda:self.pcSelectionView()).grid(column=self.MIDDLE_PANE_COLUMN+2, row=0, sticky=N, padx=10, columnspan=2)
		ttk.Button(npcSelectionView, text='Main', bootstyle=ttk.LIGHT, command=lambda:self.goToMainMenu(root)).grid(column=self.MIDDLE_PANE_COLUMN+4, row=0, sticky=N, padx=10, columnspan=2)
		selectedMonsterListbox = Listbox(npcSelectionView, width=35, height=self.LISTBOX_HEIGHT)
		selectedMonsterListbox.grid(column=self.MIDDLE_PANE_COLUMN, row=self.LISTBOX_ROW, rowspan=100, sticky=N, columnspan=6)
		if self.selectedNPCs:
			for monster in self.selectedNPCs:
				selectedMonsterListbox.insert(0, monster.name)

		'''
			RIGHT SEPARATOR: continue button
		'''
		ttk.Button(npcSelectionView, text='Continue', bootstyle=ttk.PRIMARY, command=lambda:self.getPCsInitiativeRollsView()).grid(column=self.RIGHT_SEPARATOR_COLUMN, row=10, sticky=S, padx=10, rowspan=20)

	def calculateInitiative(self, pcInitView, allInitEntries, allInitLabels, startCombatBtn):
		startCombatBtn['state'] = 'normal'
		for label in allInitLabels:
			labelRow = label.grid_info()['row']
			for pc in self.selectedPCs:
				if pc.name == label['text'].lower():
					pc.initiative = int([x for x in allInitEntries if x.grid_info()['row']==labelRow][0].get()) + pc.dex_bonus
					ttk.Label(pcInitView, text=pc.initiative, font=self.tertiaryTitleFont).grid(column=2, row=labelRow, sticky=N, pady=5, padx=5)

	def getPCsInitiativeRollsView(self):
		root.geometry('400x250')
		pcInitView = ttk.Frame(root, padding='3 3 12 12')
		pcInitView.grid(column=0, row=0, sticky=(N, W, E, S))
		root.title('PC Initiative Rolls')
		ttk.Label(pcInitView, text='PC Initiative Rolls', font=self.primaryTitleFont).grid(column=0, row=0, sticky=N, columnspan=4)
		ttk.Label(pcInitView, text='Roll', font=self.tertiaryTitleFont).grid(column=1, row=1, sticky=N)
		ttk.Label(pcInitView, text='Total', font=self.tertiaryTitleFont).grid(column=2, row=1, sticky=N, padx=5)
		row = 2
		allInitEntries = []
		allInitLabels = []
		for pc in self.selectedPCs:
			initLabel = ttk.Label(pcInitView, text=self.capitalizeName(pc.name), font=self.tertiaryTitleFont)
			initLabel.grid(column=0, row=row, sticky=E, pady=5)
			allInitLabels.append(initLabel)
			initStr = StringVar()
			initEntry = Entry(pcInitView, textvariable=initStr, width=3)
			initEntry.grid(column=1, row=row, pady=5)
			allInitEntries.append(initEntry)
			row+=1		
		startCombatBtn = ttk.Button(pcInitView, text='Start Combat', state='disabled', bootstyle=ttk.DANGER, command=lambda:self.getNewCombatNameView())
		startCombatBtn.grid(column=3, row=row+1, sticky=S, pady=10, padx=5, columnspan=2)
		ttk.Button(pcInitView, text='Calculate Initiative', bootstyle=ttk.INFO, command=lambda:self.calculateInitiative(pcInitView, allInitEntries, allInitLabels, startCombatBtn)).grid(column=1, row=row+1, sticky=S, pady=10, padx=5, columnspan=2)
		ttk.Button(pcInitView, text='Back', bootstyle=ttk.DARK, command=lambda:self.npcSelectionView()).grid(column=4, row=0, sticky=E, padx=(100,0))

	def getNewCombatNameView(self):
		root.geometry('300x200')
		newCombatNameView = ttk.Frame(root, padding='3 3 12 12')
		newCombatNameView.grid(column=0, row=0, sticky=(N, W, E, S))
		root.title('Combat Name')
		'''
			Get combat name
		'''
		ttk.Label(newCombatNameView, text='Combat Name', font=self.secondaryTitleFont).grid(column=0, row=0, sticky=(N), pady=10, columnspan=2)
		combatName = StringVar()
		combatNameEntry = Entry(newCombatNameView, textvariable=combatName, width=30)
		combatNameEntry.grid(column=0, row=2, sticky=N, padx=5, pady=(10,0), columnspan=2)

		ttk.Button(newCombatNameView, text='Back', bootstyle=ttk.DARK, command=lambda:self.npcSelectionView()).grid(column=0, row=3, sticky=S, padx=10, pady=10)
		ttk.Button(newCombatNameView, text='Continue', bootstyle=ttk.PRIMARY, command=lambda:self.newCombatView(combatName)).grid(column=1, row=3, sticky=S, pady=10)

	def listboxSearch(self, monsterListbox, NPCList, search_str):
		sstr = search_str.get()
		monsterListbox.delete(0, 'end')
		if sstr == '':
			self.fillListbox(NPCList, monsterListbox)
			return
		filteredData = list()
		for monster in NPCList:
			if monster.find(sstr) >= 0:
				filteredData.append(monster)
		self.fillListbox(filteredData, monsterListbox)

	def fillListbox(self, ld, monsterListbox):
		for npc in ld:
			monsterListbox.insert('end', self.capitalizeName(npc))

	def capitalizeName(self, fullName):
		return ' '.join([name.capitalize() for name in fullName.split(' ')])

	def addSelectedNPC(self, monsterListbox, selectedMonsterListbox, NPCList):
		selectedMonster = monsterListbox.get(monsterListbox.curselection()).lower()
		selectedMonsterListbox.insert(0, self.capitalizeName(selectedMonster))
		numOfSameType = 1
		for previouslySelectedNPC in self.selectedNPCs:
			if selectedMonster == previouslySelectedNPC.name.lower():
				numOfSameType += 1
		for npcName in NPCList:
			if npcName == selectedMonster:
				with open('monsters.csv', newline='') as monsterFile:
					monsterReader = csv.reader(monsterFile, delimiter=',')
					for row in monsterReader:
						if row[0] == npcName:
							if numOfSameType > 1:
								npcObj = Character(self.capitalizeName(npcName + str(numOfSameType)), row[1], False)
							else:
								npcObj = Character(self.capitalizeName(npcName), row[1], False)
							self.selectedNPCs.append(npcObj)

	def removeSelectedNPC(self, selectedMonsterListbox, NPCList):
		selectedMonster = selectedMonsterListbox.get(selectedMonsterListbox.curselection()).lower()
		for char in NPCList:
			if char.name == selectedMonster:
				self.selectedNPCs.remove(char)
		selectedMonsterListbox.delete(selectedMonsterListbox.curselection())

	def addSelectedPC(self, selectedPCsListbox, availableListbox):
		selectedPC = availableListbox.get(availableListbox.curselection())
		selectedPCsListbox.insert(0, selectedPC)
		for pc in self.unselectedPCs:
			if pc.name == selectedPC:
				self.selectedPCs.append(pc)
				self.unselectedPCs.remove(pc)
		availableListbox.delete(availableListbox.curselection())

	def removeSelectedPC(self, selectedPCsListbox, availableListbox):
		selectedPC = selectedPCsListbox.get(selectedPCsListbox.curselection()).lower()
		availableListbox.insert(0, self.capitalizeName(selectedPC))
		for pc in self.selectedPCs:
			if pc.name == selectedPC:
				self.selectedPCs.remove(pc)
				self.unselectedPCs.append(pc)
		selectedPCsListbox.delete(selectedPCsListbox.curselection())

	def combatSelectionView(self, root, mainMenu):
		mainMenu.destroy()
		existing = ttk.Frame(root, padding='3 3 12 12')
		existing.grid(column=0, row=0, sticky=(N, W, E, S))
		root.geometry('340x200')

		combat_selection_dict, file_selection_dict = display_combat_options(5, True)
		list_of_combats = [*combat_selection_dict.values()]
		longest_string = 0
		for combat in list_of_combats:
			if len(combat) > longest_string:
				longest_string = len(combat)
		
		ttk.Label(existing, text='Select A Combat', font=self.primaryTitleFont).grid(column=0, row=0, sticky=S, columnspan=4)
		listbox_choiced = StringVar(value=list_of_combats)
		combat_selection_box = Listbox(existing, width=longest_string, height=len(list_of_combats), listvariable=listbox_choiced)
		combat_selection_box.grid(column=0, row=1, sticky=(N,E), columnspan=4)
		ttk.Button(existing, text='Select', bootstyle=ttk.INFO, command=lambda:self.existingCombatView(combat_selection_box, file_selection_dict, root, existing)).grid(column=0, row=2, sticky=W, pady=5, columnspan=2)
		ttk.Button(existing, text='Main', bootstyle=ttk.LIGHT, command=lambda:self.goToMainMenu(root)).grid(column=3, row=2, sticky=W, pady=5, columnspan=2)
	
	def displayPreviousRounds(self, roundNum, roundActions, listbox):
		if listbox.get(0, 'end'):
			# remove most recent round
			if listbox.get(0, 'end')[-2] == roundNum:
				listbox.delete('end')
				listbox.delete('end')
		listbox.insert('end', roundNum)
		listbox.insert('end', roundActions)

	def moveUpInitiativeOrder(self, initOrderListbox):
		try:
			index = initOrderListbox.curselection()
			index = index[0]
			if not index or index == 0:
				return
			text=initOrderListbox.get(index)
			initOrderListbox.delete(index)
			initOrderListbox.insert(index-1, text)
			initOrderListbox.pop(index)
			initOrderListbox.insert(index-1, text)
			initOrderListbox.selection_set(index-1)
			initOrderListbox.selection_anchor(index-1)
		except:
			pass

	def moveDownInitiativeOrder(self, initOrderListbox):
		try:
			index = initOrderListbox.curselection()
			index = index[0]
			if (not index and index != 0) or index == initOrderListbox.index("end")-1:
				return
			text=initOrderListbox.get(index)
			initOrderListbox.delete(index)
			initOrderListbox.insert(index+1, text)
			initOrderListbox.pop(index)
			initOrderListbox.insert(index+1, text)
			initOrderListbox.selection_set(index+1)
			initOrderListbox.selection_anchor(index+1)
		except:
			pass

	def newCombatView(self, combatName):
		root.geometry('1000x500')
		newCombatView = ttk.Frame(root, padding='3 3 12 12')
		newCombatView.grid(column=0, row=0, sticky=(N, W, E, S))
		root.title('Combat Manager - {}'.format(combatName.get()))
		combat = Combat(combatName.get())

		'''
			Calculate NPC initiative
		'''
		for npc in self.selectedNPCs:
			npc.initiative = get_npc_init(npc.dex_bonus)

		'''
			Determine initiative order
		'''
		combat.combatants.extend(self.selectedPCs)
		combat.combatants.extend(self.selectedNPCs)
		combat.combatants.sort(key=lambda x:x.initiative, reverse=True)
		combatants = tiebreaker(combat.combatants, True)

		ttk.Separator(newCombatView, orient=VERTICAL).grid(column=self.LEFT_SEPARATOR_COLUMN, row=self.PANE_LABEL_ROW, ipady=500, padx=15, rowspan=50)
		ttk.Separator(newCombatView, orient=VERTICAL).grid(column=self.RIGHT_SEPARATOR_COLUMN, row=self.PANE_LABEL_ROW, ipady=500, padx=15, rowspan=50)
		'''
			LEFT: listbox and scrollbar
		'''
		ttk.Label(newCombatView, text='Previous Rounds', font=self.secondaryTitleFont).grid(column=self.LEFT_PANE_COLUMN, row=self.PANE_LABEL_ROW, sticky=N, columnspan=6)
		prevRoundListbox = Listbox(newCombatView, width=35, height=self.LISTBOX_HEIGHT)
		prevRoundListbox.grid(column=self.LEFT_PANE_COLUMN, row=self.LISTBOX_ROW, rowspan=100, sticky=N, columnspan=6)
		xScrollbar = Scrollbar(newCombatView, orient=HORIZONTAL)
		xScrollbar.grid(row=self.LISTBOX_SCROLLBAR_ROW, column=0, columnspan=6, sticky=(N,E,W))
		prevRoundListbox.config(xscrollcommand=xScrollbar.set)
		xScrollbar.config(command=prevRoundListbox.xview)

		'''
			RIGHT: listbox/initiative order
		'''
		ttk.Label(newCombatView, text='Initiative Order', font=self.secondaryTitleFont).grid(column=self.RIGHT_PANE_COLUMN, row=self.PANE_LABEL_ROW, sticky=N, columnspan=6)
		initOrderListbox = Listbox(newCombatView, width=45, height=self.LISTBOX_HEIGHT)
		initOrderListbox.grid(column=self.RIGHT_PANE_COLUMN, row=self.LISTBOX_ROW-1, rowspan=100, sticky=N, columnspan=6)
		for combatant in combatants:
			initOrderListbox.insert('end', combatant)

		ttk.Button(newCombatView, text='Main', bootstyle=ttk.LIGHT, command=lambda:self.goToMainMenu(root)).grid(column=self.RIGHT_PANE_COLUMN+10, row=0, sticky=N)
		ttk.Button(newCombatView, text='Up', bootstyle=ttk.LIGHT, command=lambda:self.moveUpInitiativeOrder(initOrderListbox)).grid(column=self.RIGHT_PANE_COLUMN+10, row=2, sticky=N)
		ttk.Button(newCombatView, text='Down', bootstyle=ttk.LIGHT, command=lambda:self.moveDownInitiativeOrder(initOrderListbox)).grid(column=self.RIGHT_PANE_COLUMN+10, row=3, sticky=N)

		'''
			MIDDLE: ROUND LABEL
		'''
		if self.roundCount == 0:
			self.roundCount = 1
		roundLabel = ttk.Label(newCombatView, text='Round ' + str(self.roundCount), font=self.secondaryTitleFont)
		roundLabel.grid(column=self.MIDDLE_PANE_COLUMN, row=self.PANE_LABEL_ROW, sticky=N, columnspan=10)
		self.roundLabelList.append(roundLabel)
		'''
			MIDDLE: COMBAT BUTTONS
		'''
		prevBtn = ttk.Button(newCombatView, state='disabled', text='Prev', command=lambda:self.goToPreviousCombatant())
		prevBtn.grid(column=self.PREV_BTN_COLUMN, row=self.ITERATE_BTN_ROW, sticky=E, ipadx=2, padx=5)
		self.allButtonsDict['prevBtn'] = prevBtn
		nextBtn = ttk.Button(newCombatView, text='Next', command=lambda:self.iterateCombatants(newCombatView, combat, prevRoundListbox))
		nextBtn.grid(column=self.NEXT_BTN_COLUMN, row=self.ITERATE_BTN_ROW, ipadx=2, padx=5)
		self.allButtonsDict['nextBtn'] = nextBtn
		combatOverBtn = ttk.Button(newCombatView, text='End Combat', bootstyle=ttk.DANGER, command=lambda:self.combatOver(combat))
		combatOverBtn.grid(column=self.COMBAT_OVER_BTN_COLUMN, row=self.ITERATE_BTN_ROW, sticky=W, ipadx=2, padx=5)
		self.allButtonsDict['combatOverBtn'] = combatOverBtn

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
		highestRoundCount = 0
		for k, v in combat.rounds.items():
			if int(k) > highestRoundCount:
				highestRoundCount = int(k)
			self.displayPreviousRounds(k, v, prevRoundListbox)
		
		combatantsList = combat.combatants
		if len(combatantsList) > len(combat.rounds[highestRoundCount]):
			self.roundCount = highestRoundCount
		else:
			self.roundCount = highestRoundCount + 1

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
		ttk.Button(combatScreen, text='Main', bootstyle=ttk.LIGHT, command=lambda:self.goToMainMenu(root)).grid(column=self.RIGHT_PANE_COLUMN+10, row=0, sticky=N)
	
	def combatOver(self, combat):
		combat.rounds[self.roundCount] = self.currentRound
		print(combat.rounds)
		write_combat_to_file(combat)
		print('combat over')
		self.goToMainMenu(root)

	def goToMainMenu(self, root):
		self.__init__(root)

	def goToPreviousCombatant(self):
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
				self.allActionTextboxes[-1]['state'] = 'normal'
				self.allActionTextboxes[-1].config(background='white')
			self.rowIndex -= 1
			self.turnIndex -= 1
		if len(self.allCombatantLabels) < 2:
			self.allButtonsDict['prevBtn']['state'] = 'disabled'

	def resumeMidRound(self, combat):
		combatantsList = combat.combatants
		if self.nextCombatantInd > self.turnIndex:
			# print('self.nextCombatantInd: ', self.nextCombatantInd)
			# print('self.turnIndex2: ', self.turnIndex)
			# required for continuing combat in which the most recent round was not completed
			if self.roundCount in combat.rounds:
				print('self.roundCount: ', self.roundCount)
				print('combat.rounds2: ', combat.rounds)
				if len(combat.rounds[self.roundCount].keys()) < len(combatantsList):
					# print('len(combat.rounds[self.roundCount].keys(): ', len(combat.rounds[self.roundCount].keys()))
					# print('len(combatantsList): ', len(combatantsList))
					for combatant in combatantsList:
						if combatant.name in combat.rounds[self.roundCount].keys():
							# print('combatant.name:
							# .roundCount].keys(): ', combat.rounds[self.roundCount].keys())
							self.nextCombatantInd = combatantsList.index(combatant) + 1
					if self.nextCombatantInd == 999:
						self.nextCombatantInd = 0
					self.turnIndex = self.nextCombatantInd

	def iterateCombatants(self, combatScreen, combat, prevRoundListbox):
		'''Print the next combatant to list of combatants on screen. 
		'''

		# first, check if combat round resuming mid-turn
		self.resumeMidRound(combat)

		# second, move existing label/text boxes/buttons down
		currentCombatant = ''
		if self.turnIndex > 0:
			for existingCombatantLabel in self.allCombatantLabels:
				row = existingCombatantLabel.grid_info()['row']
				currentCombatant = existingCombatantLabel['text']
				if currentCombatant not in self.currentRound:
					self.currentRound[currentCombatant] = ''
				existingCombatantLabel.grid(column=self.MIDDLE_PANE_COLUMN, row=row+2, sticky=W, rowspan=2, columnspan=2)

		if self.turnIndex > 0:
			for existingActionTextbox in self.allActionTextboxes:
				row = existingActionTextbox.grid_info()['row']
				# get action of currentCombatant
				self.currentRound[currentCombatant] = existingActionTextbox.get('1.0', 'end')[:-1]
				existingActionTextbox.grid(column=self.MIDDLE_PANE_COLUMN+2, row=row+2, sticky=E, rowspan=2, columnspan=8)
				existingActionTextbox.config(background='#f0f0f0')
			
		# third, check if round over
		combatantsList = combat.combatants
		if self.turnIndex == len(combatantsList):
			# update combat object
			combat.rounds[self.roundCount] = self.currentRound
			# update previous rounds panel
			self.displayPreviousRounds(self.roundCount, combat.rounds[self.roundCount], prevRoundListbox)
			# update round label
			self.roundCount += 1
			self.roundLabelList[0].config(text='Round ' + str(self.roundCount))
			# reset some variables
			self.turnIndex = 0
			self.currentRound = {}
			# remove previous round label/boxes from middle panel
			for existingCombatantLabel in self.allCombatantLabels:
				existingCombatantLabel.grid_remove()
			for existingActionTextbox in self.allActionTextboxes:
				existingActionTextbox.grid_remove()
			self.allCombatantLabels.clear()
			self.allActionTextboxes.clear()

		# fourth, add new label/textbox
		print('combatantsList: ', combatantsList)
		print('self.turnIndex: ', self.turnIndex)
		newCombatantLabel = ttk.Label(combatScreen, text=combatantsList[self.turnIndex].name, font=self.tertiaryTitleFont)
		newCombatantLabel.grid(column=self.MIDDLE_PANE_COLUMN, row=2, sticky=W, rowspan=2, columnspan=2)
		self.allCombatantLabels.append(newCombatantLabel)
		newActionTextbox = Text(combatScreen, width=25, height=2)
		newActionTextbox.grid(column=self.MIDDLE_PANE_COLUMN+2, row=2, sticky=E, rowspan=2, columnspan=8)
		self.allActionTextboxes.append(newActionTextbox)
		newActionTextbox.focus_set()

		# fifth, change state of prev button
		if len(self.allCombatantLabels) < 2:
			self.allButtonsDict['prevBtn']['state'] = 'disabled'
		else:
			self.allButtonsDict['prevBtn']['state'] = 'normal'

		# sixth, update variables
		self.rowIndex += 1
		self.turnIndex += 1
		
root = Tk()
CombatManager(root)
root.mainloop()