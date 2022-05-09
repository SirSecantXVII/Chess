from fnmatch import translate
import chess
import config
import fenparser
import math
import sys
import mayn
import pygame as p

Depth = int(input("What depth would you like to use"))
num = 1
length = 8

def AiThinking(board):
    tree = Node(Depth, num, 0, board) # creates the decison tree
    move = min_max(Depth, tree, num, -sys.maxsize, sys.maxsize)
    board.push(move[1])
    return board

def calcPieceValue(piece, colour, Rrow, Rcol):
    piece = piece.upper()
    pst_pos = (length * Rrow) + Rcol
    position_scores = config.pst[piece]
    position_scores = position_scores[::-1] #this reverses the scores so they can be processed correctly

    if colour == True:
        piece_value = config.piece[piece]
        pst_value = position_scores[pst_pos]  # whites eval is set as positive "inf" so its objective is to make the score more postive
    else:
        piece_value = -config.piece[piece] # blacks eval is set as negative "inf" so its objective is to make the score more negative
        pst_value = -position_scores[pst_pos]
    return pst_value + piece_value

def calculate_score_for_position(Rrow, Rcol, fen): # CALCULATES THE value of each piece on the board
    piece = fen[Rrow][Rcol]

    if piece == "P":
        return calcPieceValue(piece, False, Rrow, Rcol)
    elif piece == "N":
        return calcPieceValue(piece, False, Rrow, Rcol)
    elif piece == "B":
        return calcPieceValue(piece, False, Rrow, Rcol)
    elif piece == "R":
        return calcPieceValue(piece, False, Rrow, Rcol)
    elif piece == "Q":
        return calcPieceValue(piece, False, Rrow, Rcol)
    elif piece == "K":
        return calcPieceValue(piece, False, Rrow, Rcol)
    elif piece == "p":
        return calcPieceValue(piece, True, Rrow, Rcol)
    elif piece == "n":
        return calcPieceValue(piece, True, Rrow, Rcol)
    elif piece == "b":
        return calcPieceValue(piece, True, Rrow, Rcol)
    elif piece == "r":
        return calcPieceValue(piece, True, Rrow, Rcol)
    elif piece == "q":
        return calcPieceValue(piece, True, Rrow, Rcol)
    elif piece == "k":
        return calcPieceValue(piece, True, Rrow, Rcol)
    else:
        p.display("Eval is 0")

def evaluate_board_score(board):
    fen = translate(board)
    score = 0 # at the start of a game the evaluation is equal
    for Rrow in range(len(fen)):
        for Rcol in range(len(fen[Rrow])):
            score += calcPieceValue(Rrow, Rcol, fen) # calculates the score of the board
    p.display("Current Eval: " + score)

def translate(board):
    return fenparser.FenParser(board.fen()).parse()

class Node():
    def __init__(self, depth, playernum, move, board):
        self.depth = depth
        self.playernum = playernum
        self.board = board
        self.move = move
        self.children = []
        self.generate_children()

    #create the tree
    def generate_children(self):
        legal_moves = [x for x in self.board.legal_moves]# all legal moves
        if self.depth >= 0:
            for x in legal_moves: # every move
                self.board.push(x) # tries every move
                self.children.append(Node(self.depth-1, -self.num, x, self.board)) # carries on appending the next move till depth = 0
                self.board.pop() # undoes the move

# algorithm xD
def min_max(depth, node, player, alpha, beta):
    if player > 0:
        max_score = [alpha, None] 
    else:
        max_score = [beta, None]

    if depth == 0:
        node.board.push(node.move)
        score = evaluate_board_score(node.board)
        node.board.pop()
        return [score, node.move]

    #Maximizer
    if player > 0:
        for child in node.children:
            child.board.push(child.move)
            evaluation = min_max(depth-1, child, -player, alpha, beta)
            child.board.pop()

            if(evaluation[0] > max_score[0]):
                #if there is no move, we are at the top of the tree
                #and needs to return the best move
                if(node.move != 0):
                    max_score = [evaluation[0], node.move]
                else:
                    max_score = [evaluation[0], evaluation[1]]

            alpha = max(max_score[0], alpha)

            #pruning
            if beta <= alpha: #prunes as it leads to a worseR position for white
                break
    #minimizer
    else: 
        for child in node.children:
            child.board.push(child.move)
            evaluation = min_max(depth-1, child, -player, alpha, beta) # as blacks aim is to create the most negative evaluation player is negative
            child.board.pop()

            if(evaluation[0] < max_score[0]):
                if(node.move != 0):
                    max_score = [evaluation[0], node.move]
                else:
                    max_score = [evaluation[0], evaluation[1]]
            
            beta = min(max_score[0], beta)
            
            #pruning
            if beta <= alpha:
                break
    return max_score