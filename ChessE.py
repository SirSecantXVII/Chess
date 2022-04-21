# for all moves and chess development for the game
from distutils.archive_util import make_archive


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

        self.moveFunct = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}

        self.whiteToMove = True #In a game of Chess, White is always first to move
        self.movelog = []#insert castling
        self.WKingLoc = (7, 4)
        self.BKingLoc = (0,4)
        self.isCheckMate = False
        self.isStalemate = False


    def makeMove(self, move):
        self.board[move.startingRow][move.startingColumn] = "xx"
        self.board[move.endingRow][move.endingColumn] = move.pieceMoved
        self.movelog.append(move) # log the move so it is abke to be undone later
        if move.pieceMoved == "wK": #if the white king is moved
            self.WKingLoc = (move.endingRow, move.endingColumn)
        elif move.pieceMoved == "bK": #if the black king is moved
            self.BKingLoc = (move.endingRow, move.endingColumn)
        self.whiteToMove = not self.whiteToMove # swap sides  i.e black to white// white to black


    def undoMove(self): # undo move
        if len(self.movelog) != 0: #make sure mopve log is not zero as it wouldnt be able to execute
            move = self.movelog.pop()
            self.board[move.startingRow][move.startingColumn ] = move.pieceMoved
            self.board[move.endingRow][move.endingColumn] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK": #if the white king is moved 
                self.WKingLoc = (move.startingRow, move.startingColumn)
            elif move.pieceMoved == "bK": #if the black king is moved
                self.BKingLoc = (move.startingRow, move.startingColumn)
    #checking valid moves
    def returnValidMove(self):
        moves = self.returnAllValidMoves()
        for x in range(len(moves)-1, -1, -1):
            self.makeMove(moves[x]) # checks opponents moves
            self.whiteToMove = not self.whiteToMove # to switch back to original
            if self.check():
                moves.remove(moves[x])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.check():
                self.isCheckMate = True
            else:
                self.isStalemate = True
        else:
            self.isCheckMate = False
            self.isStalemate = False
        return moves

    def check(self):
        if self.whiteToMove:
            return self.FindAttackedSquare(self.WKingLoc[0], self.WKingLoc[1])
        else:
            return self.FindAttackedSquare(self.BKingLoc[0], self.BKingLoc[1])

    def FindAttackedSquare(self,r ,c):
        self.whiteToMove = not self.whiteToMove # generate all opponents moves
        oMoves = self.returnAllValidMoves()
        for move in oMoves:
            if move.endingRow == r and move.endingColumn == c:
                self.whiteToMove = not self.whiteToMove
                return True
        self.whiteToMove = not self.whiteToMove
        return False

    # all moves without considering if results/creates a check
    def returnAllValidMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): # number of columns in each row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunct[piece](r, c, moves)# calls the right funct
        return moves

    #gets all pawn moves for the pawn at row,column and add to movelog
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # white pawn
            if self.board[r-1][c] == "xx": #one square pawn movement
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "xx": #2 square pawn advancement
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: #left capture
                if self.board[r-1][c-1][0] == "b": #enemy piece for le capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # right capture
                if self.board[r-1][c+1][0] == "b": #enemy piece
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        
        else: # i can use an else statement as its just balck and white that are playing in turns
            if self.board[r+1][c] == "xx": #one square pawn movement
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "xx": #2 square pawn advancement
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0: #left capture
                if self.board[r+1][c-1][0] == "w": #enemy piece for le capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # right capture
                if self.board[r+1][c+1][0] == "w": #enemy piece
                    moves.append(Move((r, c), (r+1, c+1), self.board))



    #gets all rook moves for the rook at row,column and add to movelog
    def getRookMoves(self, r, c, moves):
        d = ((-1,0),(0,-1),(1,0),(0,1))
        ecolour = "b" if self.whiteToMove else "w"
        for w in d:
            for i in range(1,8):
                endingRow = r + w[0] * i
                endingColumn = c + w[1] * i
                if 0 <= endingRow < 8 and 0 <= endingColumn < 8: #on the board
                    endP = self.board[endingRow][endingColumn]
                    if endP == "xx": # empty space invalid
                        moves.append(Move((r,c),(endingRow, endingColumn), self.board))
                    elif endP[0] == ecolour: # enemy p
                        moves.append(Move((r,c),(endingRow, endingColumn), self.board))
                        break
                    else:
                        break
                else: #off the board
                    break


    #gets all Knight moves for the Knight at row,column and add to movelog
    def getKnightMoves(self, r, c, moves):
        kMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        ffc = "w" if self.whiteToMove else "b"
        for k in kMoves:
            endingRow = r + k[0]
            endingColumn = c + k[1]
            if 0 <= endingRow < 8 and 0 <= endingColumn < 8: #on the board
                endP = self.board[endingRow][endingColumn]
                if endP[0] != ffc:
                    moves.append(Move((r,c),(endingRow, endingColumn), self.board))




    #gets all Bishop moves for the Bishop at row,column and add to movelog
    def getBishopMoves(self, r, c, moves):
        d = ((-1,-1),(-1,1),(1,-1),(1,1))
        ecolour = "b" if self.whiteToMove else "w"
        for w in d:
            for i in range(1,8):
                endingRow = r + w[0] * i
                endingColumn = c + w[1] * i
                if 0 <= endingRow < 8 and 0 <= endingColumn < 8: #on the board
                    endP = self.board[endingRow][endingColumn]
                    if endP == "xx": # empty space invalid
                        moves.append(Move((r,c),(endingRow, endingColumn), self.board))
                    elif endP[0] == ecolour: # enemy p
                        moves.append(Move((r,c),(endingRow, endingColumn), self.board))
                        break
                    else:
                        break
                else: #off the board
                    break

    #gets all Queen moves for the Queen at row,column and add to movelog
    def getQueenMoves(self, r, c, moves):
        # a queen can move both like a biushop and like a rook so we can just use those functions
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    #gets all King moves for either King at row,column and add to movelog
    def getKingMoves(self, r, c, moves):
        # a king can only move to adjacent squares and one square diagonally
        KingM = ((-1, -1),(-1, 0),(-1,1),(0, -1),(0, 0),(0, 1),(1, -1),(1, 0),(1,1))
        ffc = "w" if self.whiteToMove else "b"
        for i in range(8):
            endR = r + KingM[i][0]
            endC = c + KingM[i][1]
            if 0 <= endR < 8 and 0 <= endC < 8: #on the board
                    endP = self.board[endR][endC]
                    if endP[0] != ffc: #not same col
                         moves.append(Move((r,c),(endR, endC), self.board))

            



class Move():
    #maps keys to values
    #key : value
    ranksToRows = {"1": 7, "2":6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
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
        self.MoveID = self.startingRow * 1000 + self.startingColumn * 100 + self.endingRow * 10 + self.endingColumn #unique moveID

#so the same move doesnt breake le code
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False


    def GetChessNotat(self):
        #to be able to make real chess pgn
        return self.getRankFile(self.startingRow, self.startingColumn) + self.getRankFile(self.endingRow, self.endingColumn)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]