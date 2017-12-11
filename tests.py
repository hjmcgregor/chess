import chess
import subprocess
from game import Game
from datetime import datetime

def main():
	args = Args()
	for i in range(1,50):
		st = datetime.now()
		board = chess.Board()
		board.set_standard()
		game = Game(args)
		# board.print_board()
		if game.white:
			game.get_move(board)
		else:
			bm = game.get_bestmove(board.get_fen(), board.turn)
			game.move(board, bm[:2], bm[2:4])
			# game.get_move(board)
			# board.print_board()
		print 'game %s took %s seconds' % (i, datetime.now()-st)

class Args(object):
	def __init__(self):
		self.e ='../stockfish-8-mac/Mac/stockfish-8-64'
		self.wsl= 15
		self.bsl= 20
		self.w= False
		self.b= False
		self.pgn= False
		self.p= False
		self.hints= False


if __name__ == "__main__":
	main()