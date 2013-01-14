import random
from copy import deepcopy

class Player:
	def __init__(self):
		self.name = raw_input("What is your name? ")
		while self.name == "":
			self.name = raw_input("I need a name for pete's sake! What is your name? ")	
	
	def choice(self, token):
		print "%s, where do you want to place your %s?" % (self.name, token)
		row, column = None, None
		while row is None and column is None:
			try:
				text = "Submit the number of the row and the column (e.g. 0 2): "
				row, column = [int(x) for x in raw_input(text).split() if int(x) in range(3)]
			except ValueError:
				print "This format is not correct. Make sure you have typed two integers between 0 and 2, separated by some blank space."
				continue
		return 3*row + column
	
	def move(self, game_entries, character):
		choice = self.choice(character)
		while game_entries[choice] != " ":
			print "Too bad, that space is taken! Try again!"
			choice = self.choice(character)
		else:
			game_entries[choice] = character
		return game_entries

class Computer:
	def __init__(self):
		if random.randint(1,2) != 1:
			self.player_picks = True
			print "Player first."
			self.player_token = "X"
			self.computer_token = "O"
		else:
			self.player_picks = False
			print "Computer first."
			self.player_token = "O"
			self.computer_token = "X"
	
	def scenario_builder(self, board, character):
		test_board = deepcopy(board)
		possible_boards = []
		for i in range(len(board)):
			if test_board[i] == " ":
				current_poss = deepcopy(test_board)
				current_poss[i] = character
				possible_boards.append(current_poss)
		return possible_boards

	def evaluate_winner(self, game_entries):
		p_win, c_win, game_over, message = False, False, False, None
		rows = [[game_entries[i+3*j] for i in range(3)] for j in range(3)]
		columns = [[game_entries[3*i+j] for i in range(3)] for j in range(3)]
		diagonals = [[game_entries[4*i] for i in range(3)], [game_entries[2+2*i] for i  in range(3)]]
		
		if True in [len(set(row)) == 1 for row in rows if self.player_token in row] or True in [len(set(column)) == 1 for column in columns if self.player_token in column] or True in [len(set(diagonal)) == 1 for diagonal in diagonals if self.player_token in diagonal]:
			message = "Player wins!"
			p_win, game_over = True, True

		elif True in [len(set(row)) == 1 for row in rows if self.computer_token in row] or True in [len(set(column)) == 1 for column in columns if self.computer_token in column] or True in [len(set(diagonal)) == 1 for diagonal in diagonals if self.computer_token in diagonal]:
			message = "Computer wins!"
			c_win, game_over = True, True
		
		elif game_over == False:
			if " " not in game_entries:
				message = "Nobody wins! It's a tie."
				game_over = True
			else:
				message = ""
		
		return game_over, p_win, c_win, message
	
	def opponent_winner_move(self, state):
		scenarios = self.scenario_builder(state, self.player_token)
		return True in [self.evaluate_winner(scenario)[1]==True for scenario in scenarios]
	
	def maximization(self, state):
		score_by_scenario = []
		for scenario in self.scenario_builder(state, self.computer_token):
			util = None
			game_over, p_win, c_win, message = self.evaluate_winner(scenario)
			if p_win:
				util = -1
			elif c_win:
				util = 1
			elif game_over:
				util = 0
			else:
				util = self.minimization(scenario)[0][1]
			score_by_scenario.append((scenario, util))
		score_by_scenario.sort(key=lambda tup: tup[1])
		return score_by_scenario

	def minimization(self, state):
		score_by_scenario = []
		for scenario in self.scenario_builder(state, self.player_token):
			util = None
			game_over, p_win, c_win, message = self.evaluate_winner(scenario)
			if p_win:
				util = -1
			elif c_win:
				util = 1
			elif game_over:
				util = 0
			else:
				util = self.maximization(scenario)[-1][1]
			score_by_scenario.append((scenario, util))
		score_by_scenario.sort(key=lambda tup: tup[1])
		return score_by_scenario

	def move(self, state):
		if state[4] == " ":
			state[4] = self.computer_token
		elif self.computer_token not in state:
			state[0] = self.computer_token
		else:
			state = self.maximization(state)[-1][0]
		return state

running = True
message = None
game_entries = [" "]*9

player = Player()
computer = Computer()
player_token = computer.player_token
player_turn = computer.player_picks

while running:
	print "\n" + "\n----------\n".join([" | ".join([game_entries[3*i+j] for j in range(3)]) for i in range(3)]) + "\n"
	game_over, p_win, c_win, message = computer.evaluate_winner(game_entries)
	if game_over:
		print message
		print "Game over!"
		running = False
	if running and player_turn:
		game_entries = player.move(game_entries, player_token)
		player_turn = not player_turn
	elif running and not player_turn:
		print "Me, the computador, haz chosen!"
		game_entries = computer.move(game_entries)
		player_turn = not player_turn