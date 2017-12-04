# python chess
A Python chess rules engine. The moves are determined using the Stockfish chess engine (https://stockfishchess.org/).

Each piece will have its own class, along with the Board class.

In order to determine a list of legal moves for a particular piece, we call the "get_moves" method of the particular piece class. We then whittle this down via the "get_legal_moves" method of the Board class, which accounts for castling, en passant, and pawn promotion logic. The "get_legal_moves" method also calls the "is_self_check" method of the board class, which projects a hypothetical move to determine if that would place the current player in self-check (which would be illegal). If that particular move is self check, it is removed from the list of legal moves.
#TODO- clean up the "is_self_check" method, which I believe generally slows everything down.

