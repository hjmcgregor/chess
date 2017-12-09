# python chess
A Python chess rules engine. Computer moves are determined using the Stockfish chess engine (https://stockfishchess.org/). You must pass the location of your stockfish engine via positional argument (examples below).


```
A python Chess rules framework, using the Stockfish chess engine.

positional arguments:
  E           Stockfish Engine location

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

Examples:

Stockfish White (level 20) vs Stockfish Black (level 15), with printing on (only including the last printed board in this example):

```
$ python game.py 'stockfish-8-mac/Mac/stockfish-8-64' -bsl 15 -p

...

Checkmate, white wins
8  ·   ·   ·   ♖   ·   ·   ♚   ·  

7  ·   ·   ·   ·   ·   ·   ·   ·  

6  ·   ·   ·   ·   ·   ·   ♔   ·  

5  ·   ·   ·   ·   ·   ·   ·   ♟  

4  ·   ·   ·   ·   ·   ·   ♟   ♙  

3  ·   ·   ·   ·   ·   ·   ♙   ·  

2  ·   ·   ·   ·   ·   ·   ·   ·  

1  ·   ·   ·   ·   ·   ·   ·   ·  

   a   b   c   d   e   f   g   h  

```

Playing as white vs. black computer (skill level 1), with hints included:
```
$ python game.py 'stockfish-8-mac/Mac/stockfish-8-64' -bsl 1 -w --hints

8  ♜   ♞   ♝   ♛   ♚   ♝   ♞   ♜  

7  ♟   ♟   ♟   ♟   ♟   ♟   ♟   ♟  

6  ·   ·   ·   ·   ·   ·   ·   ·  

5  ·   ·   ·   ·   ·   ·   ·   ·  

4  ·   ·   ·   ·   ·   ·   ·   ·  

3  ·   ·   ·   ·   ·   ·   ·   ·  

2  ♙   ♙   ♙   ♙   ♙   ♙   ♙   ♙  

1  ♖   ♘   ♗   ♕   ♔   ♗   ♘   ♖  

   a   b   c   d   e   f   g   h  

(Best move via stockfish: d2d4)
white, enter your move: d2d4
8  ♜   ♞   ♝   ♛   ♚   ♝   ♞   ♜  

7  ♟   ♟   ♟   ♟   ♟   ♟   ♟   ♟  

6  ·   ·   ·   ·   ·   ·   ·   ·  

5  ·   ·   ·   ·   ·   ·   ·   ·  

4  ·   ·   ·   ♙   ·   ·   ·   ·  

3  ·   ·   ·   ·   ·   ·   ·   ·  

2  ♙   ♙   ♙   ·   ♙   ♙   ♙   ♙  

1  ♖   ♘   ♗   ♕   ♔   ♗   ♘   ♖  

   a   b   c   d   e   f   g   h  

8  ♜   ♞   ♝   ♛   ♚   ♝   ♞   ♜  

7  ♟   ♟   ♟   ·   ♟   ♟   ♟   ♟  

6  ·   ·   ·   ♟   ·   ·   ·   ·  

5  ·   ·   ·   ·   ·   ·   ·   ·  

4  ·   ·   ·   ♙   ·   ·   ·   ·  

3  ·   ·   ·   ·   ·   ·   ·   ·  

2  ♙   ♙   ♙   ·   ♙   ♙   ♙   ♙  

1  ♖   ♘   ♗   ♕   ♔   ♗   ♘   ♖  

   a   b   c   d   e   f   g   h  

(Best move via stockfish: e2e4)
white, enter your move: 

```

# Rules Logic

In order to determine a list of legal moves for a particular piece, we call the "get_moves" method of the particular piece object. We then whittle this down via the "get_legal_moves" method of the Board class, which accounts for castling, en passant, and pawn promotion logic. The "get_legal_moves" method also calls the "is_self_check" method of the board class, which projects a hypothetical move to determine if that would place the current player in self-check (which would be illegal). If that particular move is self check, it is removed from the list of legal moves.
