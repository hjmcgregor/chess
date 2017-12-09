# python chess
A Python chess rules engine. The moves are determined using the Stockfish chess engine (https://stockfishchess.org/).
```
usage: game.py [-h] [-bsl BSL] [-wsl WSL] [-w] [-b] [-p] [--hints]

A python Chess rules framework, using the Stockfish chess engine.

optional arguments:
  -h, --help  show this help message and exit
  -bsl BSL    the skill level for Black (0 to 20). Default is 20
  -wsl WSL    the skill level for White (0 to 20). Default is 20
  -w          White user. Default is computer. Include this if you want a
              human to make moves for white.
  -b          Black user. Default is computer. Include this if you want a
              human to make moves for black.
  -p          Turn on board printing
  --hints     Turn on hints
```

Example:

Stockfish White (level 20) vs Stockfish Black (level 15), with printing on (only including the last printed board in this example):

```
python game.py -bsl 15 -p

...

Checkmate, white wins
8  ·   ·   ·   ·   ·   ♔   ·   ♛  

7  ·   ·   ·   ·   ·   ·   ·   ·  

6  ·   ·   ·   ♚   ♝   ·   ♟   ·  

5  ·   ·   ·   ·   ·   ·   ·   ·  

4  ·   ·   ·   ·   ·   ·   ·   ·  

3  ·   ·   ·   ·   ·   ·   ·   ·  

2  ·   ·   ·   ·   ·   ·   ·   ·  

1  ·   ·   ·   ·   ·   ·   ·   ·  

   a   b   c   d   e   f   g   h 

```

Rules Logic

In order to determine a list of legal moves for a particular piece, we call the "get_moves" method of the particular piece object. We then whittle this down via the "get_legal_moves" method of the Board class, which accounts for castling, en passant, and pawn promotion logic. The "get_legal_moves" method also calls the "is_self_check" method of the board class, which projects a hypothetical move to determine if that would place the current player in self-check (which would be illegal). If that particular move is self check, it is removed from the list of legal moves.
