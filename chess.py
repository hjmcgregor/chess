#!/usr/bin/python
# -*- coding: utf-8 -*-
from pprint import pprint
from datetime import datetime
import copy



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
		# halfmove number
		self.hm = 0
		# fullmove number
		self.fm = 1
		# en passant
		self.ep = '-'
		self.log = []
		# the fen array
		self.fens = []


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


	def find_pos(self, piece):
		for pos, p in self.positions.items():
			if p == piece:
				return pos

	def is_self_check(self, piece, np):
		r = False
		op = piece.get_pos(self)
		tp = self.positions[np]
		self.positions[op] = None
		self.positions[np] = piece
		if self.is_check():
			r = True
		self.positions[op] = piece
		self.positions[np] = tp

		return r


	def update_board(self, piece, np):
		# TODO: clean up the en passant logic
		# TODO: add current game's moves to PGN array

		# !=0 here to avoid going through this if it is only for hypothetical purposes
		if piece.get_pos(self) != 0:
			self.update_ep(piece, np)
			self.update_hm(piece, np)
			self.update_fm(piece, np)

			# finally, update the board positions while accounting for castling
			if piece.n == 'K' and piece.num_moves == 0:
				# white kingside castle
				if piece.get_pos(self) == 'e1' and np == 'g1':
					self.positions[np] = piece
					self.positions['f1'] = self.positions['h1']
					self.positions['e1'] = None
					self.positions['h1'] = None
					# update the Rook's num_moves, since only the King's will get updated in this method
					self.positions['f1'].num_moves += 1
				# white queenside castle
				elif piece.get_pos(self) == 'e1' and np == 'c1':
					self.positions[np] = piece
					self.positions['d1'] = self.positions['a1']
					self.positions['e1'] = None
					self.positions['a1'] = None
					self.positions['d1'].num_moves += 1
				# black kingside castle
				elif piece.get_pos(self) == 'e8' and np == 'g8':
					self.positions[np] = piece
					self.positions['f8'] = self.positions['h8']
					self.positions['e8'] = None
					self.positions['h8'] = None
					self.positions['f8'].num_moves += 1
				# black queenside castle
				elif piece.get_pos(self) == 'e8' and np == 'c8':
					self.positions[np] = piece
					self.positions['d8'] = self.positions['a8']
					self.positions['e8'] = None
					self.positions['a8'] = None
					self.positions['d8'].num_moves += 1
				else:
					self.positions[piece.get_pos(self)] = None
					self.positions[np] = piece
				piece.num_moves += 1
			# and queen promotion
			elif piece.n == 'p' and (int(np[1]) == 8 or int(np[1]) == 1):
				if piece.c == 'w':
						self.positions[piece.get_pos(self)] = None
						self.positions[np] = Q('w')
				elif piece.c == 'b':
						self.positions[piece.get_pos(self)] = None
						self.positions[np] = Q('b')			
			else:
				self.positions[piece.get_pos(self)] = None
				self.positions[np] = piece


	def get_legal_moves(self, piece):
		# make a deep copy of each object here, so we don't update the board or the pieces with our hypothetical
		# moves
		mv = piece.get_moves(self)
		# print piece.get_pos(self), mv
		lm = []

		# this is to avoid self-check
		for m in mv:
			if not self.is_self_check(piece, m):
				lm.append(m)
			# nb = copy.deepcopy(self)
			# np = copy.deepcopy(piece)
			# # print np
			# nb.update_board(np, m)
		
			# find your own King's position first
			# kp = nb.find_king(np.c)
			# kp = self.find_king(piece.c)

			# now if your King's position appears in the opponent's possible moves, it is self check
			# opp_moves = []
			# opp_moves = self.get_opp_moves(piece.c)
			# print "opp moves: ", opp_moves

			# if piece.n != 'K' and kp not in opp_moves:
			# 	lm.append(m)
			# elif np.n == 'K' and m not in opp_moves:
			# 	lm.append(m)

			# del nb
			# del np
			# print piece.n, lm, "opp_moves: ", opp_moves
		# now append squares for castling, while accounting for positions that are threatened
		if piece.n == 'K':
			cur_cas = self.castling()
			# squares that cannot be threatened
			wkt = ['e1', 'f1', 'g1', 'h1']
			wqt = ['a1', 'b1', 'c1', 'd1', 'e1']
			bqt = ['a8', 'b8', 'c8', 'd8', 'e8']
			bkt = ['e8', 'f8', 'g8', 'h8']
			opp_moves = self.get_opp_moves(piece.c)
			if piece.get_pos(self) == 'e1':
				# white kingside castling
				if 'K' in cur_cas:
					if not self.is_occupied('f1') and not self.is_occupied('g1'):
						if not any(x in wkt for x in opp_moves):
							lm.append('g1')
				# white queenside castling
				if 'Q' in cur_cas:
					if not self.is_occupied('b1') and not self.is_occupied('c1') and not self.is_occupied('d1'):
						if not any(x in wqt for x in opp_moves):
							lm.append('c1')
			if piece.get_pos(self) == 'e8':
				# black kingside castling
				if 'k' in cur_cas:
					if not self.is_occupied('f8') and not self.is_occupied('g8'):
						if not any(x in bkt for x in opp_moves):
							lm.append('g8')
				# black queenside castling
				if 'q' in cur_cas:
					if not self.is_occupied('b8') and not self.is_occupied('c8') and not self.is_occupied('d8'):
						if not any(x in bqt for x in opp_moves):
							lm.append('c8')

		if piece.n == 'p':
			# if the en-passant attribute is in an adjacent file, it is a legal move
			if piece.c == 'w' and int(piece.get_pos(self)[1]) == 5:
				if piece.get_pos(self)[0] == 'a' and self.ep == 'b6':
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'b' and (self.ep == 'a6' or self.ep == 'c6'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'c' and (self.ep == 'b6' or self.ep == 'd6'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'd' and (self.ep == 'c6' or self.ep == 'e6'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'e' and (self.ep == 'd6' or self.ep == 'f6'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'f' and (self.ep == 'e6' or self.ep == 'g6'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'g' and (self.ep == 'f6' or self.ep == 'h6'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'h' and self.ep == 'g6':
					lm.append(self.ep)
			if piece.c == 'b' and int(piece.get_pos(self)[1]) == 4:
				if piece.get_pos(self)[0] == 'a' and self.ep == 'b3':
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'b' and (self.ep == 'a3' or self.ep == 'c3'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'c' and (self.ep == 'b3' or self.ep == 'd3'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'd' and (self.ep == 'c3' or self.ep == 'e3'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'e' and (self.ep == 'd3' or self.ep == 'f3'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'f' and (self.ep == 'e3' or self.ep == 'g3'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'g' and (self.ep == 'f3' or self.ep == 'h3'):
					lm.append(self.ep)
				if piece.get_pos(self)[0] == 'h' and self.ep == 'g3':
					lm.append(self.ep)
		# print piece.get_pos(self), lm
		return lm


	def update_hm(self, piece, np):
		# update the halfmove clock
		if piece.n == 'p' or self.positions[np] != None:
			self.hm = 0
		else:
			self.hm += 1


	def update_fm(self, piece, np):
		# and the fullmove clock
		if self.turn == 'b':
			self.fm += 1


	def update_ep(self, piece, np):
		# update the fen en passant string
		if piece.n == 'p':
			if piece.c == 'b' and (int(piece.get_pos(self)[1]) - int(np[1])) == 2:
				if np[0] == 'a':
					if self.positions['b5'] is not None and self.positions['b5'].n == 'p' and self.positions['b5'].c == 'w':
						self.ep = 'a6'
				elif np[0] == 'b':
					if self.positions['a5'] is not None and self.positions['a5'].n == 'p' and self.positions['a5'].c == 'w':
						self.ep = 'b6'
					if self.positions['c5'] is not None and self.positions['c5'].n == 'p' and self.positions['c5'].c == 'w':
						self.ep = 'b6'
				elif np[0] == 'c':
					if self.positions['b5'] is not None and self.positions['b5'].n == 'p' and self.positions['b5'].c == 'w':
						self.ep = 'c6'
					if self.positions['d5'] is not None and self.positions['d5'].n == 'p' and self.positions['d5'].c == 'w':
						self.ep = 'c6'
				elif np[0] == 'd':
					if self.positions['c5'] is not None and self.positions['c5'].n == 'p' and self.positions['c5'].c == 'w':
						self.ep = 'd6'
					if self.positions['e5'] is not None and self.positions['e5'].n == 'p' and self.positions['e5'].c == 'w':
						self.ep = 'd6'
				elif np[0] == 'e':
					if self.positions['d5'] is not None and self.positions['d5'].n == 'p' and self.positions['d5'].c == 'w':
						self.ep = 'e6'
					if self.positions['f5'] is not None and self.positions['f5'].n == 'p' and self.positions['f5'].c == 'w':
						self.ep = 'e6'
				elif np[0] == 'f':
					if self.positions['e5'] is not None and self.positions['e5'].n == 'p' and self.positions['e5'].c == 'w':
						self.ep = 'f6'
					if self.positions['g5'] is not None and self.positions['g5'].n == 'p' and self.positions['g5'].c == 'w':
						self.ep = 'f6'
				elif np[0] == 'g':
					if self.positions['f5'] is not None and self.positions['f5'].n == 'p' and self.positions['f5'].c == 'w':
						self.ep = 'g6'
					if self.positions['f5'] is not None and self.positions['f5'].n == 'p' and self.positions['f5'].c == 'w':
						self.ep = 'g6'
				elif np[0] == 'h':
					if self.positions['g5'] is not None and self.positions['g5'].n == 'p' and self.positions['g5'].c == 'w':
						self.ep = 'h6'
			elif piece.c == 'w' and (int(np[1]) - int(piece.get_pos(self)[1])) == 2:
				if np[0] == 'a':
					if self.positions['b4'] is not None and self.positions['b4'].n == 'p' and self.positions['b4'].c == 'b':
						self.ep = 'a3'
				elif np[0] == 'b':
					if self.positions['a4'] is not None and self.positions['a4'].n == 'p' and self.positions['a4'].c == 'b':
						self.ep = 'b3'
					if self.positions['c4'] is not None and self.positions['c4'].n == 'p' and self.positions['c4'].c == 'b':
						self.ep = 'b3'
				elif np[0] == 'c':
					if self.positions['b4'] is not None and self.positions['b4'].n == 'p' and self.positions['b4'].c == 'b':
						self.ep = 'c3'
					if self.positions['d4'] is not None and self.positions['d4'].n == 'p' and self.positions['d4'].c == 'b':
						self.ep = 'c3'
				elif np[0] == 'd':
					if self.positions['c4'] is not None and self.positions['c4'].n == 'p' and self.positions['c4'].c == 'b':
						self.ep = 'd3'
					if self.positions['e4'] is not None and self.positions['e4'].n == 'p' and self.positions['e4'].c == 'b':
						self.ep = 'd3'
				elif np[0] == 'e':
					if self.positions['d4'] is not None and self.positions['d4'].n == 'p' and self.positions['d4'].c == 'b':
						self.ep = 'e3'
					if self.positions['f4'] is not None and self.positions['f4'].n == 'p' and self.positions['f4'].c == 'b':
						self.ep = 'e3'
				elif np[0] == 'f':
					if self.positions['e4'] is not None and self.positions['e4'].n == 'p' and self.positions['e4'].c == 'b':
						self.ep = 'f3'
					if self.positions['g4'] is not None and self.positions['g4'].n == 'p' and self.positions['g4'].c == 'b':
						self.ep = 'f3'
				elif np[0] == 'g':
					if self.positions['f4'] is not None and self.positions['f4'].n == 'p' and self.positions['f4'].c == 'b':
						self.ep = 'g3'
					if self.positions['f4'] is not None and self.positions['f4'].n == 'p' and self.positions['f4'].c == 'b':
						self.ep = 'g3'
				elif np[0] == 'h':
					if self.positions['g4'] is not None and self.positions['g4'].n == 'p' and self.positions['g4'].c == 'b':
						self.ep = 'h3'
		else:
			self.ep = '-'


	def print_board(self):
		p = { 'w': { 'R':'♖', 'N':'♘', 'B':'♗', 'Q':'♕', 'K':'♔', 'p':'♙'},
				'b': { 'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'p':'♟'}
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


	def is_rep_draw(self, fen):
		self.fens.append(fen.split(' ')[0] + fen.split(' ')[2] + fen.split(' ')[3])
		if self.fens.count(fen.split(' ')[0] + fen.split(' ')[2] + fen.split(' ')[3]) > 2:
			return True
		else:
			return False


	def is_stalemate(self):
		# stalemate conditions, as per http://www.e4ec.org/immr.html
		# get all of each color's pieces
		p = {'w': [], 'b': []}
		for pos, piece in self.positions.items():
			if piece is not None:
				if piece.c == 'w':
					p['w'].append(piece)
				else:
					p['b'].append(piece)

		# K v K stalemate
		if len(p['w']) == 1 and len(p['b']) == 1:
			if p['w'][0].n == 'K' and p['b'][0].n == 'K':
				return True

		# if there are no legal moves, but are not in check
		lm = 0
		for piece in p[self.turn]:
			lm += len(self.get_legal_moves(piece))
		if lm == 0 and not self.is_check():
			return True

		# bishop & king vs. king, knight & king vs. king
		# we'll ignore the situation for now where a player promotes to a same-color bishop
		if len(p['w']) == 1 and len(p['b']) == 2:
			if p['w'][0].n == 'K':
				if (p['b'][0].n == 'K' and p['b'][1].n == 'B') or (p['b'][0].n == 'B' and p['b'][1].n == 'K'):
					return True
				elif (p['b'][0].n == 'K' and p['b'][1].n == 'N') or (p['b'][0].n == 'N' and p['b'][1].n == 'K'):
					return True
		if len(p['w']) == 2 and len(p['b']) == 1:
			if p['b'][0].n == 'K':
				if (p['w'][0].n == 'K' and p['w'][1].n == 'B') or (p['w'][0].n == 'B' and p['w'][1].n == 'K'):
					return True
				if (p['w'][0].n == 'K' and p['w'][1].n == 'N') or (p['w'][0].n == 'N' and p['w'][1].n == 'K'):
					return True


	def is_check(self):
		n = self.get_opp_moves(self.turn)
		kp = self.find_king(self.turn)
		if kp in n:
			return True
		else:
			return False


	def is_checkmate(self):
		lm = 0
		for pos, p in self.positions.items():
			if p is not None and p.c == self.turn:
				m = self.get_legal_moves(p)
				lm = lm + len(m)
		if lm == 0:
			return True
		else:
			return False


	def update_turn(self):
		if self.turn == 'w':
			self.turn = 'b'
		else:
			self.turn = 'w'


	def castling(self):
		"""Returns the castling ability as a fen string"""
		fen = ""
		wkr = self.positions['h1']
		wk = self.positions['e1']
		wqr = self.positions['a1']

		bkr = self.positions['h8']
		bk = self.positions['e8']
		bqr = self.positions['a8']

		if wkr is not None and wk is not None:
			if wkr.c == 'w' and wkr.n == 'R' and wk.c == 'w' and wk.n == 'K':
				if wkr.num_moves == 0 and wk.num_moves == 0:
					fen += "K"
		if wqr is not None and wk is not None:
			if wqr.c == 'w' and wqr.n == 'R' and wk.c == 'w' and wk.n == 'K':
				if wqr.num_moves == 0 and wk.num_moves == 0:
					fen += "Q"
		if bkr is not None and bk is not None:
			if bkr.c == 'b' and bkr.n == 'R' and bk.c == 'b' and bk.n == 'K':
				if bkr.num_moves == 0 and bk.num_moves == 0:
					fen += "k"
		if bqr is not None and bk is not None:
			if bqr.c == 'b' and bqr.n == 'R' and bk.c == 'b' and bk.n == 'K':
				if bqr.num_moves == 0 and bk.num_moves == 0:
					fen += "q"

		if len(fen) == 0:
			fen = "-"

		return fen


	def get_fen(self):
		fen = ""
		yr = [i for i in range(8,0,-1)]
		
		for i in yr:
			c = 0
			for n in self.x:
				if self.positions[n + str(i)] is not None:
					if c > 0:
						fen += str(c)
						c = 0
					if self.positions[n + str(i)].c == 'w':
						fen += self.positions[n + str(i)].n.upper()
					else:
						fen += self.positions[n + str(i)].n.lower()
				else:
					c += 1
				if self.x.index(n) == 7 and c > 0:
					fen += str(c)
			if i > 0:
				fen += "/"
		fen += " " + self.turn
		fen += " " + self.castling()
		fen += " " + self.ep
		fen += " " + str(self.hm)
		fen += " " + str(self.fm)

		return fen



class R(object):
	"""Rook"""
	def __init__(self, color):
		self.c = color
		self.n = "R"
		# for castling
		self.num_moves = 0

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
		return board.find_pos(self)


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
		return board.find_pos(self)


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
		return board.find_pos(self)


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
		return board.find_pos(self)


class K(object):
	"""King"""
	def __init__(self, color):
		self.c = color
		self.n = "K"
		# for castling
		self.num_moves = 0

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
		return board.find_pos(self)


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
				if not board.is_occupied(board.x[board.x.index(cx)] + str(cy + 1)) and not board.is_occupied(np):
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
				if not board.is_occupied(board.x[board.x.index(cx)] + str(cy - 1)) and not board.is_occupied(np):
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
		return board.find_pos(self)


