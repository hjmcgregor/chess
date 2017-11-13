#!/usr/bin/python
from pprint import pprint


class Board:
	"""The board Class"""
	def __init__(self):
		self.x = ['a','b','c','d','e','f','g','h']
		self.y = [i for i in range(1,9)]
		self.positions = {}
		for n in self.x:
			for i in self.y:
				# rooks
				if n == 'a' or n == 'h':
					if i == 1:
						self.positions[n + str(i)] = R('w', n + str(i))
					elif i == 8:
						self.positions[n + str(i)] = R('b', n + str(i))
				# knights
				elif n == 'b' or n == 'g':
					if i == 1:
						self.positions[n + str(i)] = N('w', n + str(i))
					elif i == 8:
						self.positions[n + str(i)] = N('b', n + str(i))
				# bishops
				elif n == 'c' or n == 'f':
					if i == 1:
						self.positions[n + str(i)] = B('w', n + str(i))
					elif i == 8:
						self.positions[n + str(i)] = B('b', n + str(i))
				# queens
				elif n == 'd':
					if i == 1:
						self.positions[n + str(i)] = Q('w', n + str(i))
					elif i == 8:
						self.positions[n + str(i)] = Q('b', n + str(i))
				# kings
				elif n == 'e':
					if i == 1:
						self.positions[n + str(i)] = K('w', n + str(i))
					elif i == 8:
						self.positions[n + str(i)] = K('b', n + str(i))
				# pawns
				if i == 2:
					self.positions[n + str(i)] = p('w', n + str(i))
				elif i == 7:
					self.positions[n + str(i)] = p('b', n + str(i))
				elif i > 2 and i <7:
					self.positions[n + str(i)] = ''


	def is_occupied(self, p):
		if self.positions[p] == '':
			return False
		else:
			return True


class R:
	"""Rook"""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def get_moves(self, board):
		t = []
		cx = self.p[0]
		cy = int(self.p[1])
		a, b, c, d = (0, 0, 0, 0)
		for i in board.y:
			if board.x.index(cx) + i <= 7:
				np = board.x[board.x.index(cx) + i] + str(cy)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and a == 0:
					t.append(np)
					a = 1
			if board.x.index(cx) - i >= 0:
				np = board.x[board.x.index(cx) - i] + str(cy)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and b == 0:
					t.append(np)
					b = 1
			if cy - i > 0:
				np = board.x[board.x.index(cx)] + str(cy - i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and c == 0:
					print np
					t.append(np)
					c = 1
			if cy + i < 9:
				np = board.x[board.x.index(cx)] + str(cy + i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and d == 0:
					t.append(np)
					d = 1

		return t


class B:
	"""Bishop"""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def get_moves(self, board):
		t = []
		cx = self.p[0]
		cy = int(self.p[1])
		a, b, c, d = (0, 0, 0, 0)
		for i in board.y:
			if board.x.index(cx) + i <= 7 and cy + i < 9:
				np = board.x[board.x.index(cx) + i] + str(cy + i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and a == 0:
					t.append(np)
					a = 1
			if board.x.index(cx) - i >= 0 and cy - i > 0:
				np = board.x[board.x.index(cx) - i] + str(cy - i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and b == 0:
					t.append(np)
					b = 1
			if board.x.index(cx) + i <= 7 and cy - i > 0:
				np = board.x[board.x.index(cx) - i] + str(cy - i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and c == 0:
					print np
					t.append(np)
					c = 1
			if board.x.index(cx) - i >= 0 and cy + i < 9:
				np = board.x[board.x.index(cx) - i] + str(cy + i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and d == 0:
					t.append(np)
					d = 1

		return t


class Q:
	"""Queen"""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def get_moves(self, board):
		# the queens moves are just a combination of a rook and a bishop
		t = []
		cx = self.p[0]
		cy = int(self.p[1])
		a, b, c, d, e, f, g, h = (0, 0, 0, 0, 0, 0, 0, 0)
		for i in board.y:
			# rook
			if board.x.index(cx) + i <= 7:
				np = board.x[board.x.index(cx) + i] + str(cy)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and a == 0:
					t.append(np)
					a = 1
			if board.x.index(cx) - i >= 0:
				np = board.x[board.x.index(cx) - i] + str(cy)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and b == 0:
					t.append(np)
					b = 1
			if cy - i > 0:
				np = board.x[board.x.index(cx)] + str(cy - i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and c == 0:
					print np
					t.append(np)
					c = 1
			if cy + i < 9:
				np = board.x[board.x.index(cx)] + str(cy + i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and d == 0:
					t.append(np)
					d = 1

			# bishop
			if board.x.index(cx) + i <= 7 and cy + i < 9:
				np = board.x[board.x.index(cx) + i] + str(cy + i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and e == 0:
					t.append(np)
					e = 1
			if board.x.index(cx) - i >= 0 and cy - i > 0:
				np = board.x[board.x.index(cx) - i] + str(cy - i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and f == 0:
					t.append(np)
					f = 1
			if board.x.index(cx) + i <= 7 and cy - i > 0:
				np = board.x[board.x.index(cx) - i] + str(cy - i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and g == 0:
					print np
					t.append(np)
					g = 1
			if board.x.index(cx) - i >= 0 and cy + i < 9:
				np = board.x[board.x.index(cx) - i] + str(cy + i)
				if not board.is_occupied(np):
					t.append(np)
				elif board.is_occupied(np) and g == 0:
					t.append(np)
					g = 1

		return t


class N:
	"""Knight"""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def get_moves(self, board):
		t = []
		cx = self.p[0]
		cy = int(self.p[1])
		if board.x.index(cx) + 1 <= 7 and cy + 2 < 9:
			np = board.x[board.x.index(cx) + 1] + str(cy + 2)
			t.append(np)
		if board.x.index(cx) + 1 <= 7 and cy - 2 > 0:
			np = board.x[board.x.index(cx) + 1] + str(cy - 2)
			t.append(np)
		if board.x.index(cx) + 2 <= 7 and cy - 1 > 0:
			np = board.x[board.x.index(cx) + 2] + str(cy - 1)
			t.append(np)
		if board.x.index(cx) + 2 <= 7 and cy + 1 < 9:
			np = board.x[board.x.index(cx) + 2] + str(cy + 1)
			t.append(np)
		if board.x.index(cx) - 2 >= 0 and cy + 1 < 9:
			np = board.x[board.x.index(cx) - 2] + str(cy + 1)
			t.append(np)
		if board.x.index(cx) - 2 >= 0 and cy - 1 > 0:
			np = board.x[board.x.index(cx) - 2] + str(cy - 1)
			t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy - 2 > 0:
			np = board.x[board.x.index(cx) - 1] + str(cy - 2)
			t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy + 2 < 9:
			np = board.x[board.x.index(cx) - 1] + str(cy + 2)
			t.append(np)

		return t


class K:
	"""King"""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def get_moves(self, board):
		t = []
		cx = self.p[0]
		cy = int(self.p[1])
		if cy + 1 < 9:
			np = board.x[board.x.index(cx)] + str(cy + 1)
			t.append(np)
		if cy - 1 > 0:
			np = board.x[board.x.index(cx)] + str(cy - 1)
			t.append(np)
		if board.x.index(cx) + 1 <= 7:
			np = board.x[board.x.index(cx) + 1] + str(cy)
			t.append(np)
		if board.x.index(cx) - 1 >= 0:
			np = board.x[board.x.index(cx) - 1] + str(cy)
			t.append(np)
		if board.x.index(cx) + 1 <= 7 and cy + 1 < 9:
			np = board.x[board.x.index(cx) + 1] + str(cy + 1)
			t.append(np)
		if board.x.index(cx) + 1 <= 7 and cy - 1 > 0:
			np = board.x[board.x.index(cx) + 1] + str(cy - 1)
			t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy - 1 > 0:
			np = board.x[board.x.index(cx) - 1] + str(cy - 1)
			t.append(np)
		if board.x.index(cx) - 1 >= 0 and cy + 1 < 9:
			np = board.x[board.x.index(cx) - 1] + str(cy + 1)
			t.append(np)

		return t

class p:
	"""Pawn"""
	def __init__(self, c, p):
		self.c = c
		self.p = p

	def get_moves(self, board):
		t = []
		cx = self.p[0]
		i = int(self.p[1])

		if self.c == 'w':
			if i == 2:
				np = board.x[board.x.index(cx)] + str(i + 2)
				if not board.is_occupied(np):
					t.append(np)
			if i + 1 < 9:
				np = board.x[board.x.index(cx)] + str(i + 1)
				if not board.is_occupied(np):
					t.append(np)
			if board.x.index(cx) - 1 >= 0 and i + 1 < 9:
				np = board.x[board.x.index(cx) - 1] + str(i + 1)
				if board.is_occupied(np):
					t.append(np)
			if board.x.index(cx) + 1 <= 7 and i + 1 < 9:
				np = board.x[board.x.index(cx) + 1] + str(i + 1)
				if board.is_occupied(np):
					t.append(np)
		else:
			if i == 7:
				np = board.x[board.x.index(cx)] + str(i - 2)
				if not board.is_occupied(np):
					t.append(np)
			if i - 1 > 0:
				np = board.x[board.x.index(cx)] + str(i - 1)
				if not board.is_occupied(np):
					t.append(np)
			if board.x.index(cx) - 1 >= 0 and i - 1 > 0:
				np = board.x[board.x.index(cx) - 1] + str(i - 1)
				if board.is_occupied(np):
					t.append(np)
			if board.x.index(cx) + 1 <= 7 and i - 1 > 0:
				np = board.x[board.x.index(cx) + 1] + str(i - 1)
				if board.is_occupied(np):
					t.append(np)
		return t






board = Board()
t = p('w', 'h6')
pos = board.positions

pos['h6'] = t
print t.__doc__, t.p
print pos['h6'].get_moves(board)
