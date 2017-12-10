import chess
import subprocess
from datetime import datetime
import sys
import argparse


def main():
	parser = argparse.ArgumentParser(description='A python Chess rules framework, using the Stockfish chess engine.')
	parser.add_argument('e', metavar='E', type=str,
                    help='Stockfish Engine location')
	parser.add_argument('-wsl', default=20, help='the skill level for White (0 to 20). Default is 20')
	parser.add_argument('-bsl', default=20, help='the skill level for Black (0 to 20). Default is 20')
	parser.add_argument('-w', action='store_true', help='White user. Default is computer. Include this if you want a human to make moves for white.')
	parser.add_argument('-b', action='store_true', help='Black user. Default is computer. Include this if you want a human to make moves for black.')
	parser.add_argument('-p', action='store_true', help='Turn on board printing')
	parser.add_argument('--hints', action='store_true', help='Turn on hints')
	parser.add_argument('-pgn', action='store_true', help='Print the game\'s PGN at the end')
	args = parser.parse_args()
	board = chess.Board()
	board.set_standard()
	game = Game(args)
	board.print_board()
	if game.white:
		game.get_move(board)
	else:
		bm = game.get_bestmove(board.get_fen(), board.turn)
		game.move(board, bm[:2], bm[2:4])
		game.get_move(board)


class Game(object):
	def __init__(self, args):
		self.E = args.e
		self.P = subprocess.Popen(self.E, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		self.bsl = args.bsl
		self.wsl = args.wsl
		self.white = args.w
		self.black = args.b
		self.pgn = args.pgn
		if self.white or self.black:
			self.p = True
		else:
			self.p = args.p
		self.hints = args.hints


	def get_move(self, board):
		if self.hints:
			print "(Best move via stockfish: " + self.get_bestmove(board.get_fen(), board.turn) + ")"
		m = raw_input(board.colors[board.turn] + ", enter your move: ")
		cp = m[:2]
		np = m[2:]
		if cp not in board.positions.keys() or np not in board.positions.keys():
			print "Enter a valid move"
			self.get_move(board)
		else:
			self.move(board, cp, np)


	def move(self, board, cp, np):
		starttime = datetime.now()
		if board.positions[cp] is not None and board.positions[cp].c == board.turn and np in board.get_legal_moves(board.positions[cp]):
			board.update_board(board.positions[cp], np)
			board.update_turn()
			if self.p:
				board.print_board()
			if board.is_rep_draw(board.get_fen()):
				print 'Draw- repeated moves!'
				self.end_game(board)
			if board.is_stalemate():
				print 'Draw- stalemate!'
				self.end_game(board)
			if board.is_check():
				if board.is_checkmate():
					if board.turn == 'w':
						print 'Checkmate, black wins'
					else:
						print 'Checkmate, white wins'
					board.pgnm += '#'
					self.end_game(board)
				if self.p:
					print 'Check!'
				# update the board's pgn move string here, so we only have to loop through the 
				# is_check method once
				board.pgnm += '+'
				# board.update_pgn()
			if (self.white and board.turn == 'w') or (self.black and board.turn == 'b'):
				self.get_move(board)
			else:
				board.update_pgn()
				bm = self.get_bestmove(board.get_fen(), board.turn)
				self.move(board, bm[:2], bm[2:4])
			# get_move(board)
		else:
			print 'illegal move, ' + board.colors[board.turn] + ' to move'
			self.get_move(board)


	def get_bestmove(self, fen, turn):
		if turn == 'w':
			sl = self.wsl
		else:
			sl = self.bsl
		self.P.stdin.write("setoption name Skill Level value " + str(sl) + "\n")
		self.P.stdin.write("position fen " + fen + "\n")
		self.P.stdin.write("go\n")
		for e in iter(self.P.stdout.readline, ' '):
			if 'bestmove' in e:
				return e.split(' ')[1].rstrip()

		return 0


	def end_game(self, board):
		board.update_pgn(end=True)
		board.print_board()
		if self.pgn:
			board.print_pgn()
		sys.exit()


if __name__ == "__main__":
	main()


# print board.get_legal_moves(board.positions['e8'])

# print datetime.now() - s
