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

    def makeMove(self, move):
        self.board[move.startingRow][move.startingColumn] == "xx"
        self.board[move.endingRow][move.startingColumn]
        self.movelog.append(move) # log the move so it is abke to be undone later
        self.whiteToMove = not self.whiteToMove # swap sides  i.e black to white// white to black

    def undoMove(self): # undo move
        if len(self.movelog) != 0: #make sure mopve log is not zero as it wouldnt be able to execute
            move = self.moveLog.pop()
            self.board[move.startingRow][move.startingColumn ] = move.pieceMoved
            self.board[move.endingRow][move.endingColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    #checking valid moves
    def returnValidMove(self):
        pass

    # all moves without considering if results/creates a check
    def returnAllValidMoves
class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1": 7, "2":6, "3": 5, "4": 4, 
    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}
    filesToCols = {"a": 0, "b":1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsquare, endsquare, board):
        self.startingRow = startsquare[0]
        self.startingColumn = startsquare[1]
        self.endingRow = endsquare[0]
        self.endingColumn = endsquare[1]
        self.pieceMoved = board[self.startingRow][self.startingColumn]
        self.pieceCaptured = board[self.endingRow][self.endingColumn]
    
    def GetChessNotat(self):
        #to be able to make real chess pgn
        return self.getRankFile(self.startingRow, self.startingColumn) + self.getRankFile(self.endingRow, self.endingColumn)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]