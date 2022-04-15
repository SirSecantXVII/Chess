# for all moves and chess development for the game
class State():
    def __init__(self):
        #self.board initialises the board as a 2 dimensional array so we can use {}
        #"xx" represents an empty space that holds no piece
        #first character shows the color of the piece/pawn, "b" or "w"
        #the second character represents the type of piece, "p" for pawn,"N" for Knight,"B" for Bishop,"R" for rook ,"Q" for Queen,"K" for King
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["xx", "xx", "xx", "xx", "xx", "xx", "xx", "xx"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True #In a game of Chess, White is always first to move
        self.movelog = []#insert castling