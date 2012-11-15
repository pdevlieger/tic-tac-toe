import random
from copy import deepcopy
import pdb

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
	
	def minimax(self, state):
		plausible_moves, score_by_scenario, winner, result = [], [], None, None
		scenarios = self.scenario_builder(state, self.computer_token)
		for scenario in scenarios:
			c_win = self.evaluate_winner(scenario)[2]
#			pdb.set_trace()
			if c_win:
				result = scenario
			else:
				if not self.opponent_winner_move(scenario):
					plausible_moves.append(scenario)
		if plausible_moves:
			for move in plausible_moves:
				score = self.maximizer(scenario)
				score_by_scenario.append((scenario, score))
				score_by_scenario.sort(key=lambda tup: tup[1])
				result = score_by_scenario[0][0]
		return result	
	
	def minimaxer(self, state):
		plausible_moves = []
		winner_move, optimal_move = None, None
		for scenario in self.scenario_builder(state, self.computer_token):
			game_over, p_win, c_win, message = self.evaluate_winner(scenario)
			if c_win:
				winner_move = scenario
			else:
				for subscenario in self.scenario_builder(scenario, self.player_token):
					plausible_move = True
					while plausible_move:
						go_local, p_win_local, c_win_local, message_local = self.evaluate_winner(subscenario)
						if p_win_local:
							plausible_move = False
				if plausible_move:
					plausible_moves.append(scenario)
				winner_move = plausible_moves[0]
		return winner_move

	def maximizer(self, state):
		util = -2
		game_over, p_win, c_win, message = self.evaluate_winner(state)
		if c_win:
			util = 1
		elif p_win:
			util = -1
		elif not p_win and not c_win and game_over:
			util = 0
		else:
			for scenario in self.scenario_builder(state, self.player_token):
				util = max(util, self.minimizer(scenario))
		return util

	def minimizer(self, state):
		util = 2
		game_over, p_win, c_win, message = self.evaluate_winner(state)
		if c_win:
			util = 1
		elif p_win:
			util = -1
		elif not p_win and not c_win and game_over:
			util = 0
		else:
			for scenario in self.scenario_builder(state, self.computer_token):
				util = min(util, self.maximizer(scenario))
		return util

	def move(self, state):
		if state[4] == " ":
			state[4] = self.computer_token
		else:
			state = self.minimax(state)
		return state

# Setting up some building stones. I should write this with a __main__
running = True
message = None
game_entries = [" ", ]*9

player = Player()
computer = Computer()
player_token = computer.player_token
player_turn = computer.player_picks

while running:
	pdb.set_trace()
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