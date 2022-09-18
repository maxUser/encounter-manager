from datetime import datetime
from random import randint
import ttkbootstrap as ttk
from tkinter import *
import calendar
import pickle
import os

def tiebreaker(combatants, gui=False):
	'''A function to break ties between characters' initiative counts and, if necessary, their dexterity bonuses.
	TODO: reduce duplicate code
	TODO: roll off tie

	Parameters
	----------
	combatants : list
		List of character objects particpating in the combat

	Returns
	-------
	combatants : list
		List of character objects particpating in the combat, in correct order
	'''
	tie_start_ind = 0
	tie_end_ind = 0
	# print_initiative_order(combatants)
	for i in range(len(combatants)):
		# get start and end indices of tied combatants in list
		# sort each tie set by dex bonus
		end_found = False
		if i < len(combatants)-1:
			if combatants[i].initiative == combatants[i+1].initiative and i == 0:
				tie_start_ind = i
			elif combatants[i].initiative == combatants[i+1].initiative and combatants[i].initiative != combatants[i-1].initiative:
				tie_start_ind = i
		if i > 0 and i < len(combatants)-1:
			if combatants[i].initiative != combatants[i+1].initiative and combatants[i].initiative == combatants[i-1].initiative:
				tie_end_ind = i
				end_found = True
		if combatants[i].initiative == combatants[i-1].initiative and i == len(combatants)-1:
			tie_end_ind = i
			end_found = True
		if end_found:
			# print('TIEBREAKER at {}'.format(combatants[tie_start_ind].initiative))
			combatants[tie_start_ind:tie_end_ind+1] = sorted(combatants[tie_start_ind:tie_end_ind+1], key=lambda x:x.dex_bonus, reverse=True) 
			# print('Between: ' + ', '.join([x.name for x in combatants[tie_start_ind:tie_end_ind+1]]))
			# search through the tied initiative set looking for tied dex bonuses
			dex_bonus_tie_start_ind = 0
			dex_bonus_tie_end_ind = 0
			# print_initiative_order(combatants)
			for j in range(tie_start_ind, tie_end_ind+1):
				# print('j: {}, tie_start:end {}:{}'.format(j, tie_start_ind, tie_end_ind))
				dex_bonus_end_found = False
				if j < tie_end_ind:
					if combatants[j].dex_bonus == combatants[j+1].dex_bonus and j == tie_start_ind:
						dex_bonus_tie_start_ind = j
					elif combatants[j].dex_bonus == combatants[j+1].dex_bonus and combatants[j].dex_bonus != combatants[j-1].dex_bonus:
						dex_bonus_tie_start_ind = j
				if j > tie_start_ind and j < tie_end_ind:
					if combatants[j].dex_bonus != combatants[j+1].dex_bonus and combatants[j].dex_bonus == combatants[j-1].dex_bonus and combatants[j].initiative == combatants[j-1].initiative:
						dex_bonus_tie_end_ind = j
						dex_bonus_end_found = True
				if combatants[j].dex_bonus == combatants[j-1].dex_bonus and j == tie_end_ind:
					dex_bonus_tie_end_ind = j
					dex_bonus_end_found = True
				if dex_bonus_end_found:
					guiDexTieList = []
					allRollOffEntries = []
					# print('ROLL OFF at {} dex bonus'.format(combatants[dex_bonus_tie_start_ind].dex_bonus))
					for m in combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1]:
						# print('m: {}, {}'.format(m.name, m.pc))
						if not m.pc:
							m.roll_off = int(randint(1,20))
							# print('{} roll: {}'.format(m.name, m.roll_off))
						else:
							guiDexTieList.append(m)
					if guiDexTieList:
						rollOffWindow = Toplevel()
						rollOffWindow.wm_title("Roll Off")
						titleLabel = ttk.Label(rollOffWindow, text='Roll Off! at initiative {} and dexterity bonus {}'.format(combatants[tie_start_ind].initiative, combatants[dex_bonus_tie_start_ind].dex_bonus))
						titleLabel.grid(row=0, column=0, columnspan=2)
						row = 1
						for dexTiedCombatant in guiDexTieList:
							rollOffLabel = ttk.Label(rollOffWindow, text=dexTiedCombatant.name)
							rollOffLabel.grid(column=0, row=row, sticky=W, pady=5)
							rollOffStr = StringVar()
							rollOffEntry = Entry(rollOffWindow, textvariable=rollOffStr, width=3)
							rollOffEntry.grid(column=1, row=row, pady=5)
							allRollOffEntries.append((dexTiedCombatant.name, rollOffEntry))
							row += 1
						wait = IntVar()
						b = ttk.Button(rollOffWindow, text="Okay", command=lambda: wait.set(1))
						b.grid(row=row, column=2)
						b.wait_variable(wait)
						for entry in allRollOffEntries:
							for x in combatants:
								if entry[0] == x.name:
									x.roll_off = int(entry[1].get())
						rollOffWindow.destroy()
					combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1] = sorted(combatants[dex_bonus_tie_start_ind:dex_bonus_tie_end_ind+1], key=lambda x:x.roll_off, reverse=True)
	return combatants

def get_npc_init(dex_bonus):
	'''Return a random number between 1 and 20 plus dexterity bonus.

	Parameters
	----------
	dex_bonus : int
		dexterity bonus

	Returns
	-------
	int
		number representing the initiative count
	'''

	return int(randint(1,20) + int(dex_bonus))

def write_combat_to_file(combat):
	'''A function which creates a file with a unique name that stores a serialized combat object.

	Parameters
	----------
	combat : Combat object
		A Combat object
	'''
	directory = 'combats'
	combatFiles = get_combat_file()
	for combatFileName in combatFiles:
		if combat.name in combatFileName:
			# delete old combat file
			filename = combatFileName[0] + '_' + combatFileName[1] + '_' + combatFileName[2].replace(' ', '_') + '.pickle'
			path = directory + '/' + filename
			os.remove(path)
	print('Saving {} to file'.format(combat.name))
	filename = datetime.now().strftime('%Y%m%d_%H%M%S_{}.pickle'.format(combat.name.replace(' ','_')))
	path = directory + '/' + filename
	try:
		with open(path, 'wb') as f:
			pickle.dump(combat, f)
	except Exception as e:
		print('Exception: ', e)

def get_combat_based_on_selection(selection_input, file_selection_dict):
	selected_file = file_selection_dict[selection_input]
	combat_file = get_combat_file(True, selected_file)
	with open('combats/' + combat_file, 'rb') as f:
		return pickle.load(f)

def get_combat_file(return_file=False, date_time=()):
	'''A function which returns combat file information (combat name, date, time) from a directory.

	Parameters
	----------
	return_file : boolean (optional, I think this parameter is unnecessary)
		Flag whether or not to return the file
	date_time : tuple
		tuple elements consisting of the date and time

	Returns
	-------
	file_info : list
		List of lists. The inner lists are comprised of a combat file name, date, and time.
	'''

	file_info = []
	directory = os.fsdecode('combats')
	for file in os.listdir(directory):
		filename = os.fsdecode(file)
		date_and_time = [filename[0:8], filename[9:15]] # returns ['20220721', '204351']
		if return_file and date_time:
			if date_time[0] == date_and_time[0] and date_time[1] == date_and_time[1]:
				return filename
		index_of_period = filename.index('.')
		file_combat_name = filename[16:index_of_period].replace('_', ' ')
		date_and_time.append(file_combat_name)
		file_info.append(date_and_time)
	return sorted(file_info, key=lambda file_info:[file_info[0],file_info[1]], reverse=True)

def display_combat_options(num_battles_displayed):
	'''A function which displays 'num_battles_displayed' most recent combats and asks the user to make a selection.

	Parameters
	----------
	num_battles_displayed : int
		The number of most recent combats to be displayed

	Returns
	-------
	
	'''

	file_info = get_combat_file() # [['20220725', '081517', 'battle of later that afternoon'],..]
	combat_selection_dict = {}
	file_selection_dict = {}

	i = 1
	for combat_file in file_info[0:num_battles_displayed]:
		combat_name = combat_file[2].title()
		combat_date = combat_file[0][0:4] + '/' + calendar.month_abbr[int(combat_file[0][4:6])] + '/' + combat_file[0][6:8]
		combat_time = combat_file[1][0:2] + ':' + combat_file[1][2:4] + ':' + combat_file[1][4:6]
		combat_select = combat_name + ' [' + combat_date + ' ' + combat_time + ']'
		combat_selection_dict[i] = combat_select
		file_selection_dict[i] = (combat_file[0], combat_file[1])
		i+=1
	return combat_selection_dict, file_selection_dict
	# print('Select from the {} most recent battles:'.format(num_battles_displayed))
	# for k, v in combat_selection_dict.items():
	# 	print(str(k) + ') ', v)
	# selection_input = get_list_selection_input(num_battles_displayed, '\nSelect a combat by list number: ')
	# selection = combat_selection_dict[selection_input]
	# print('You have selected: ' + selection)
	# return selection_input, file_selection_dict