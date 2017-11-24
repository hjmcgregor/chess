#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
from datetime import datetime
import copy
import sys


class Board(object):
	"""The board Class"""
	def __init__(self, t='w'):
		self.x = ['a','b','c','d','e','f','g','h']
		self.y = [i for i in range(1,9)]
		self.turn = t
		self.colors = { 'w': 'white', 'b': 'black'}
		self.positions = {}
		for n in self.x:
			for i in self.y:
				self.positions[n + str(i)] = None


	def set_standard(self):
		for n in self.x:
			for i in self.y:
				# rooks
				if n == 'a' or n == 'h':
					if i == 1:
						self.positions[n + str(i)] = R('w')
					elif i == 8:
						self.positions[n + str(i)] = R('b')
				# knights
				elif n == 'b' or n == 'g':
					if i == 1:
						self.positions[n + str(i)] = N('w')
					elif i == 8:
						self.positions[n + str(i)] = N('b')
				# bishops
				elif n == 'c' or n == 'f':
					if i == 1:
						self.positions[n + str(i)] = B('w')
					elif i == 8:
						self.positions[n + str(i)] = B('b')
				# queens
				elif n == 'd':
					if i == 1:
						self.positions[n + str(i)] = Q('w')
					elif i == 8:
						self.positions[n + str(i)] = Q('b')
				# kings
				elif n == 'e':
					if i == 1:
						self.positions[n + str(i)] = K('w')
					elif i == 8:
						self.positions[n + str(i)] = K('b')
				# pawns
				if i == 2:
					self.positions[n + str(i)] = p('w')
				elif i == 7:
					self.positions[n + str(i)] = p('b')


	def is_occupied(self, p):
		return False if self.positions[p] is None else True


	def get_opp_moves(self, color):
		t = []
		for pos, p in self.positions.items():
			m = []
			if p is not None and p.c != color:
				m = p.get_moves(self)
				t = t + m
		return t


	def find_king(self, color):
		for pos, piece in self.positions.items():
			if piece is not None and piece.c == color and piece.n == "K":
				return pos
		return 0


	def find_piece(self, piece):
		for pos, p in self.positions.items():
			if p == piece:
				return pos
		return 0


	def update_board(self, piece, np):
		# TODO: add current game's moves to an array
		# also, maybe something for castling?
		self.positions[piece.get_pos(board)] = None
		self.positions[np] = piece


	def get_legal_moves(self, piece):
		mv = piece.get_moves(board)
		lm = []
		for m in mv:
			nb = copy.deepcopy(self)
			nb.update_board(piece, m)
			# find your own King's position first
			kp = nb.find_king(piece.c)
			# now if your King's position appears in the opponent's possible moves, it is self check
			opp_moves = nb.get_opp_moves(piece.c)
			if kp not in opp_moves:
				lm.append(m)
		return lm


	def print_board(self):
		p = { 'b': { 'R':'♖', 'N':'♘', 'B':'♗', 'Q':'♕', 'K':'♔', 'p':'♙'},
				'w': { 'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'p':'♟'}
	 	  	}
 	  	x = self.x

		for i in range(8,0,-1):
			print i,
			for n in x:
				if self.positions[n + str(i)] == None:
					print ' · ',
				else:
					print ' ' + p[self.positions[n + str(i)].c][self.positions[n + str(i)].n] + ' ',
			print "\n"
		print ' ',
		for n in x:
			print ' ' + n + ' ',
		print "\n"


	def move(self, cp, np):
		starttime = datetime.now()
		if self.positions[cp] is not None and self.positions[cp].c == self.turn and np in self.get_legal_moves(self.positions[cp]):
			self.update_board(self.positions[cp], np)
			self.update_turn()
			self.print_board()
			if self.is_check():
				if self.is_checkmate():
					if self.turn == 'w':
						print 'Checkmate, black wins'
					else:
						print 'Checkmate, white wines'
					sys.exit()
				else:
					print 'Check!'
			print self.colors[self.turn] + ' to move'
			self.get_move()
		else:
			print 'illegal move, ' + self.colors[self.turn] + ' to move'
			self.get_move()
		

	def is_check(self):
		starttime = datetime.now()
		n = self.get_opp_moves(self.turn)
		kp = self.find_king(self.turn)
		print datetime.now() - starttime
		if kp in n:
			return True
		else:
			return False


	def is_checkmate(self):
		starttime = datetime.now()
		lm = 0
		for pos, p in self.positions.items():
			if p is not None and p.c == self.turn:
				m = self.get_legal_moves(p)
				lm = lm + len(m)
		print datetime.now() - starttime
		if lm == 0:
			return True
		else:
			return False


	def update_turn(self):
		if self.turn == 'w':
			self.turn = 'b'
		else:
			self.turn = 'w'


	def get_move(self):
		m = raw_input(self.colors[self.turn] + ", enter your move: ")
		cp = m[:2]
		np = m[2:]
		if cp not in self.positions.keys() or np not in self.positions.keys():
			print "Enter a valid move"
			self.get_move()
		else:
			self.move(cp, np)


class R(object):
	"""Rook"""
	def __init__(self, color):
		self.c = color
		self.n = "R"

	def get_moves(self, board):
		t = []
		cx = self.get_pos(board)[0]
		cy = int(self.get_pos(board)[1])

		a, b, c, d = (0, 0, 0, 0)
		for i in board.y:
			if board.x.index(cx) + i <= 7:
				np = board.x[board.x.index(cx) + i] + str(cy)
				if not board.is_occupied(np) and a == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and a == 0:
					a = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and a == 0:
					t.append(np)
					a = 1
			if board.x.index(cx) - i >= 0:
				np = board.x[board.x.index(cx) - i] + str(cy)
				if not board.is_occupied(np) and b == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and b == 0:
					b = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and b == 0:
					t.append(np)
					b = 1
			if cy - i > 0:
				np = board.x[board.x.index(cx)] + str(cy - i)
				if not board.is_occupied(np) and c == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and c == 0:
					c = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and c == 0:
					t.append(np)
					c = 1
			if cy + i < 9:
				np = board.x[board.x.index(cx)] + str(cy + i)
				if not board.is_occupied(np) and d == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and d == 0:
					d = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and d == 0:
					t.append(np)
					d = 1

		return t


	def get_pos(self, board):
		return board.find_piece(self)


class B(object):
	"""Bishop"""
	def __init__(self, color):
		self.c = color
		self.n = "B"

	def get_moves(self, board):
		t = []
		cx = self.get_pos(board)[0]
		cy = int(self.get_pos(board)[1])

		a, b, c, d = (0, 0, 0, 0)
		for i in board.y:
			if board.x.index(cx) + i <= 7 and cy + i < 9:
				np = board.x[board.x.index(cx) + i] + str(cy + i)
				if not board.is_occupied(np) and a == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and a == 0:
					a = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and a == 0:
					t.append(np)
					a = 1
			if board.x.index(cx) - i >= 0 and cy - i > 0:
				np = board.x[board.x.index(cx) - i] + str(cy - i)
				if not board.is_occupied(np) and b == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and b == 0:
					b = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and b == 0:
					t.append(np)
					b = 1
			if board.x.index(cx) + i <= 7 and cy - i > 0:
				np = board.x[board.x.index(cx) + i] + str(cy - i)
				if not board.is_occupied(np) and c == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and c == 0 :
					c = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and c == 0:
					t.append(np)
					c = 1
			if board.x.index(cx) - i >= 0 and cy + i < 9:
				np = board.x[board.x.index(cx) - i] + str(cy + i)
				if not board.is_occupied(np) and d == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and d == 0 :
					d = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and d == 0:
					t.append(np)
					d = 1

		return t


	def get_pos(self, board):
		return board.find_piece(self)


class Q(object):
	"""Queen"""
	def __init__(self, color):
		self.c = color
		self.n = "Q"

	def get_moves(self, board):
		# the queens moves are just a combination of a rook and a bishop
		t = []
		cx = self.get_pos(board)[0]
		cy = int(self.get_pos(board)[1])

		a, b, c, d, e, f, g, h = (0, 0, 0, 0, 0, 0, 0, 0)
		for i in board.y:
			# rook
			if board.x.index(cx) + i <= 7:
				np = board.x[board.x.index(cx) + i] + str(cy)
				if not board.is_occupied(np) and a == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and a == 0:
					a = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and a == 0:
					t.append(np)
					a = 1
			if board.x.index(cx) - i >= 0:
				np = board.x[board.x.index(cx) - i] + str(cy)
				if not board.is_occupied(np) and b == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and b == 0:
					b = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and b == 0:
					t.append(np)
					b = 1
			if cy - i > 0:
				np = board.x[board.x.index(cx)] + str(cy - i)
				if not board.is_occupied(np) and c == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and c == 0:
					c = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and c == 0:
					t.append(np)
					c = 1
			if cy + i < 9:
				np = board.x[board.x.index(cx)] + str(cy + i)
				if not board.is_occupied(np) and d == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and d == 0:
					d = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and d == 0:
					t.append(np)
					d = 1

			# bishop
			if board.x.index(cx) + i <= 7 and cy + i < 9:
				np = board.x[board.x.index(cx) + i] + str(cy + i)
				if not board.is_occupied(np) and e == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and e == 0:
					e = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and e == 0:
					t.append(np)
					e = 1
			if board.x.index(cx) - i >= 0 and cy - i > 0:
				np = board.x[board.x.index(cx) - i] + str(cy - i)
				if not board.is_occupied(np) and f == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and f == 0:
					f = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and f == 0:
					t.append(np)
					f = 1
			if board.x.index(cx) + i <= 7 and cy - i > 0:
				np = board.x[board.x.index(cx) + i] + str(cy - i)
				if not board.is_occupied(np) and g == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and g == 0:
					g = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and g == 0:
					t.append(np)
					g = 1
			if board.x.index(cx) - i >= 0 and cy + i < 9:
				np = board.x[board.x.index(cx) - i] + str(cy + i)
				if not board.is_occupied(np) and h == 0:
					t.append(np)
				elif board.is_occupied(np) and board.positions[np].c == self.c and h == 0:
					h = 1
				elif board.is_occupied(np) and board.positions[np].c != self.c and h == 0:
					t.append(np)
					h = 1

		return t


	def get_pos(self, board):
		return board.find_piece(self)


class N(object):
	"""Knight"""
	def __init__(self, color):
		self.c = color
		self.n = "N"

	def get_moves(self, board):
		t = []
		cx = self.get_pos(board)[0]
		cy = int(self.get_pos(board)[1])

		if board.x.index(cx) + 1 <= 7 and cy + 2 < 9:
			np = board.x[board.x.index(cx) + 1] + str(cy + 2)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) + 1 <= 7 and cy - 2 > 0:
			np = board.x[board.x.index(cx) + 1] + str(cy - 2)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) + 2 <= 7 and cy - 1 > 0:
			np = board.x[board.x.index(cx) + 2] + str(cy - 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) + 2 <= 7 and cy + 1 < 9:
			np = board.x[board.x.index(cx) + 2] + str(cy + 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 2 >= 0 and cy + 1 < 9:
			np = board.x[board.x.index(cx) - 2] + str(cy + 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 2 >= 0 and cy - 1 > 0:
			np = board.x[board.x.index(cx) - 2] + str(cy - 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy - 2 > 0:
			np = board.x[board.x.index(cx) - 1] + str(cy - 2)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy + 2 < 9:
			np = board.x[board.x.index(cx) - 1] + str(cy + 2)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)

		return t


	def get_pos(self, board):
		return board.find_piece(self)


class K(object):
	"""King"""
	def __init__(self, color):
		self.c = color
		self.n = "K"

	def get_moves(self, board):
		t = []
		cx = self.get_pos(board)[0]
		cy = int(self.get_pos(board)[1])

		if cy + 1 < 9:
			np = board.x[board.x.index(cx)] + str(cy + 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if cy - 1 > 0:
			np = board.x[board.x.index(cx)] + str(cy - 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) + 1 <= 7:
			np = board.x[board.x.index(cx) + 1] + str(cy)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 1 >= 0:
			np = board.x[board.x.index(cx) - 1] + str(cy)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) + 1 <= 7 and cy + 1 < 9:
			np = board.x[board.x.index(cx) + 1] + str(cy + 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) + 1 <= 7 and cy - 1 > 0:
			np = board.x[board.x.index(cx) + 1] + str(cy - 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy - 1 > 0:
			np = board.x[board.x.index(cx) - 1] + str(cy - 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy + 1 < 9:
			np = board.x[board.x.index(cx) - 1] + str(cy + 1)
			if not board.is_occupied(np) or (board.is_occupied(np) and board.positions[np].c != self.c):
				t.append(np)

		return t


	def get_pos(self, board):
		return board.find_piece(self)


class p(object):
	"""Pawn"""
	def __init__(self, color):
		self.c = color
		self.n = "p"

	def get_moves(self, board):
		t = []
		cx = self.get_pos(board)[0]
		cy = int(self.get_pos(board)[1])

		if self.c == 'w':
			if cy == 2:
				np = board.x[board.x.index(cx)] + str(cy + 2)
				if not board.is_occupied(np):
					t.append(np)
			if cy + 1 < 9:
				np = board.x[board.x.index(cx)] + str(cy + 1)
				if not board.is_occupied(np):
					t.append(np)
			if board.x.index(cx) - 1 >= 0 and cy + 1 < 9:
				np = board.x[board.x.index(cx) - 1] + str(cy + 1)
				if board.is_occupied(np) and board.positions[np].c != self.c:
					t.append(np)
			if board.x.index(cx) + 1 <= 7 and cy + 1 < 9:
				np = board.x[board.x.index(cx) + 1] + str(cy + 1)
				if board.is_occupied(np) and board.positions[np].c != self.c:
					t.append(np)
		else:
			if cy == 7:
				np = board.x[board.x.index(cx)] + str(cy - 2)
				if not board.is_occupied(np):
					t.append(np)
			if cy - 1 > 0:
				np = board.x[board.x.index(cx)] + str(cy - 1)
				if not board.is_occupied(np):
					t.append(np)
			if board.x.index(cx) - 1 >= 0 and cy - 1 > 0:
				np = board.x[board.x.index(cx) - 1] + str(cy - 1)
				if board.is_occupied(np) and board.positions[np].c != self.c:
					t.append(np)
			if board.x.index(cx) + 1 <= 7 and cy - 1 > 0:
				np = board.x[board.x.index(cx) + 1] + str(cy - 1)
				if board.is_occupied(np) and board.positions[np].c != self.c:
					t.append(np)
		return t


	def get_pos(self, board):
		return board.find_piece(self)

# s = datetime.now()
board = Board()
board.set_standard()
# board.positions['d8'] = Q('w')
# board.positions['d1'] = Q('b')
board.print_board()
board.get_move()

# print datetime.now() - s
