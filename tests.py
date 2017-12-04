import chess
import subprocess
from datetime import datetime
import sys


E = '../Stockfish/src/stockfish'
P = subprocess.Popen(E, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def main():

	# s = datetime.now()
	board = chess.Board()
	board.set_standard()
	# board.positions['f6'] = chess.K('w')
	# board.positions['g6'] = chess.N('w')
	# board.positions['g8'] = chess.B('w')
	# board.positions['f8'] = chess.K('b')
	board.print_board()

	bm = get_bestmove(board.get_fen())
	move(board, bm[:2], bm[2:4])
	get_move(board)
	


def get_move(board):
	m = raw_input(board.colors[board.turn] + ", enter your move: ")
	cp = m[:2]
	np = m[2:]
	
	if cp not in board.positions.keys() or np not in board.positions.keys():
		print "Enter a valid move"
		get_move(board)
	else:
		move(board, cp, np)


def move(board, cp, np):
	starttime = datetime.now()
	if board.positions[cp] is not None and board.positions[cp].c == board.turn and np in board.get_legal_moves(board.positions[cp]):
		board.update_board(board.positions[cp], np)
		board.print_board()
		board.update_turn()
		if board.is_rep_draw(board.get_fen()):
			print 'Draw- repeated moves!'
			sys.exit()
		if board.is_stalemate():
			print 'Draw- stalemate!'
			sys.exit()
		if board.is_check():
			if board.is_checkmate():
				if board.turn == 'w':
					print 'Checkmate, black wins'
				else:
					print 'Checkmate, white wins'
				sys.exit()
			else:
				print 'Check!'
		print board.get_fen()
		print board.colors[board.turn] + ' to move'
		bm = get_bestmove(board.get_fen())
		print '(best move via stockfish: ' + bm + ')'
		move(board, bm[:2], bm[2:4])
		# get_move(board)
	else:
		print 'illegal move, ' + board.colors[board.turn] + ' to move'
		get_move(board)


def get_bestmove(fen):
	P.stdin.write("position fen " + fen + "\n")
	P.stdin.write("go\n")
	for e in iter(P.stdout.readline, ' '):
		if 'bestmove' in e:
			return e.split(' ')[1].rstrip()

	return 0


if __name__ == "__main__":
	main()


# print board.get_legal_moves(board.positions['e8'])

# print datetime.now() - s
