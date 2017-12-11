import chess
import subprocess
from game import Game

def main():
	args = Args()
	for i in range(0,1000):
		board = chess.Board()
		board.set_standard()
		game = Game(args)
		# board.print_board()
		if game.white:
			game.get_move(board)
		else:
			try:
				bm = game.get_bestmove(board.get_fen(), board.turn)
				game.move(board, bm[:2], bm[2:4])
				# game.get_move(board)
			except KeyboardInterrupt:
				board.print_board()

class Args(object):
	def __init__(self):
		self.e ='../stockfish-8-mac/Mac/stockfish-8-64'
		self.wsl= 20
		self.bsl= 20
		self.w= False
		self.b= False
		self.pgn= False
		self.p= False
		self.hints= False

if __name__ == "__main__":
	main()