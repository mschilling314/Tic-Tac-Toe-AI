import common


class maxer:
	person = None


class typer:
	type = True


def finished_game(board):
	# get the status of the game
	res1 = common.game_status(board)
	# if X won return true that game is done & X
	if res1 == common.constants.X:
		return True, common.constants.X
	# if O won return true that game is done & O
	if res1 == common.constants.O:
		return True, common.constants.O
	# otherwise we need to check to see that the game has finished
	for y in range(3):
		for x in range(3):
			if common.get_cell(board, y, x) == common.constants.NONE:
				# if even 1 cell is None, we're not done
				return False, common.constants.NONE
	# but if there isn't a None, we have a tie
	return True, common.constants.NONE


def parse_victor(finale):
	# start on assumption opponent won
	res = -1
	# if in fact I won, utility is 1
	if finale == maxer.person:
		res = 1
	# if in fact it was a tie, utility is 0
	elif finale == common.constants.NONE:
		res = 0
	return res


def get_empty_pos(board):
	res = []
	# iterate over every pos on the board
	for y in range(3):
		for x in range(3):
			# if the pos is empty, append it to res
			if common.get_cell(board, y, x) == common.constants.NONE:
				res.append([y, x])
	return res


def get_next_turn(turn):
	# if it's X's turn then make it O's
	if turn == common.constants.X:
		return common.constants.O
	# if it's O's turn then make it X's
	elif turn == common.constants.O:
		return common.constants.X


def prune(board, turn, a, b):
	# first, check to see if the game is over
	fin = finished_game(board)
	# if it is, then parse the victor and return utility
	if fin[0]:
		return parse_victor(fin[1])
	# otherwise
	# if the turn goes to me we do max
	if turn == maxer.person:
		# this is essentially -inf since utility in {-1, 0, 1}
		v = -2
		# now we get the empty positions
		posns = get_empty_pos(board)
		# for each position we do recursion
		for p in posns:
			# take the turn
			common.set_cell(board, p[0], p[1], turn)
			# find the next player
			n = get_next_turn(turn)
			# continue gameplay having made the turn
			value = prune(board, n, a, b)
			# if we've found a better path, say so
			if value > v:
				v = value
			# undo our turn so we can look at the next turn
			common.set_cell(board, p[0], p[1], common.constants.NONE)
			# if we're doing a-b pruning (typer) then if v >= b return
			if v >= b and typer.type:
				return v
			# if v is better than the previous best, set a
			if v > a:
				a = v
	# if it's my opponent's turn we do min
	else:
		# this is essentially inf since utility in {-1, 0, 1}
		v = 2
		# we get all of the possible moves
		posns = get_empty_pos(board)
		# for each possible move we search
		for p in posns:
			# make the move
			common.set_cell(board, p[0], p[1], turn)
			# switch whose turn it is
			n = get_next_turn(turn)
			# recurse
			value = prune(board, n, a, b)
			# if the path is worse for me, my opponent wants to take it
			if value < v:
				v = value
			# undo their turn so we can look at the next possibility
			common.set_cell(board, p[0], p[1], common.constants.NONE)
			# if we're doing a-b pruning then if v <=a return
			if v <= a and typer.type:
				return v
			# if this is worse than the previous worst, update b
			if v < b:
				b = v
		# this is meant to deal with exiting the loops for turns prior to final
	return v


def minmax_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
	# turn off a-b pruning
	typer.type = False
	# store who I am
	maxer.person = turn
	# assume it's a tie initially
	res = common.constants.NONE
	# get our utility
	v = prune(board, turn, -2, 2)
	# if our opponent won, set res to that
	if v == -1:
		res = get_next_turn(turn)
	# if we won set res to that
	elif v == 1:
		res = turn
	# return who won
	return res

def abprun_tictactoe(board, turn):
	#put your code here:
	#it must return common.constants.X(1), common.constants.O(2) or common.constants.NONE(0) for tie.
	#use the function common.game_status(board), to evaluate a board
	#it returns common.constants.X(1) if X wins, common.constants.O(2) if O wins or common.constants.NONE(0) if tie or game is not finished
	#the program will keep track of the number of boards evaluated
	typer.type = True
	# store who I am
	maxer.person = turn
	# assume it's a tie initially
	res = common.constants.NONE
	# get our utility
	v = prune(board, turn, -2, 2)
	# if our opponent won, set res to that
	if v == -1:
		res = get_next_turn(turn)
	# if we won set res to that
	elif v == 1:
		res = turn
	# return who won
	return res
