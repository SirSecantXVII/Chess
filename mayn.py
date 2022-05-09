import chess
from tkinter import *
from matplotlib.ft2font import HORIZONTAL, VERTICAL
#board creation and dimensions
import pygame as p
import math
import fenparser
import config as cfg
import evaluation
#main file
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess game is 8x8
square_size = HEIGHT // DIMENSION
IMAGES = []



    



class CBoard():
    def __init__(self):
        self.board = chess.Board()
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = p.time.Clock()
        p.display.set_caption("Chess Engine")
        self.FirstPosition = None
        self.LastPosition = None
        self.LoadImages()
        self.WTurn = True

    
    def LoadImages(self):
        pieces = ["WhiteP", "BlackP", "WhiteN", "BlackN", "WhiteR", "BlackR", "WhiteK", "BlackK", "WhiteQ", "BlackQ", "WhiteB", "BlackB", "yello"]
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("pieceimages/" + piece + ".png"), (square_size, square_size))
        self.WhiteP = IMAGES[0]
        self.BlackP = IMAGES[1]
        self.WhiteN = IMAGES[2]
        self.BlackN = IMAGES[3]
        self.WhiteR = IMAGES[4]
        self.BlackR = IMAGES[5]
        self.WhiteK = IMAGES[6]
        self.BlackK = IMAGES[7]
        self.WhiteQ = IMAGES[8]
        self.BlackQ = IMAGES[9]
        self.WhiteB = IMAGES[10]
        self.BlackB = IMAGES[11]
        self.highlight = IMAGES[12]
        #loads all the images into an array

    def ConvertToSquare(self, HORIZONTAL, VERTICAL):
        Rrow = 7 - int(math.floor(VERTICAL/square_size)) #flips the Rrow so we can translate it to fen 
        Rcol = int(math.floor(HORIZONTAL/square_size))# squares are 1x1
        return chess.square(Rcol, Rrow) 

    def convert_to_board_coordinates(self, Rrow, Rcolumn):
        HORIZONTAL = Rrow * (HEIGHT/DIMENSION)#this is so it says relative to the screen size
        VERTICAL = Rcolumn * (WIDTH/DIMENSION)
        return (HORIZONTAL, VERTICAL)

    def drawBoard(self, screen):
        colours = [p.Color("white"), p.Color("brown")]
        for Rrow in range(DIMENSION):
            for Rcol in range(DIMENSION):
                color = colours[((Rrow+Rcol) % 2)]#alternating
                p.draw.rect(self.screen, color, p.Rect(Rcol*square_size, Rrow*square_size, square_size, square_size))
        
        if self.FirstPosition:
            Rrow = self.find_row(self.FirstPosition)
            Rcol = self.find_column(self.FirstPosition)

            (HORIZONTAL, VERTICAL) = self.convert_to_board_coordinates(Rcol, Rrow)
            VERTICAL = HEIGHT - (VERTICAL + square_size) 
            self.screen.blit(self.highlight, (HORIZONTAL, VERTICAL))
    
    def draw_pieces(self, fen):
        for x in range(DIMENSION * DIMENSION):
            Rcol = int(math.floor(x / DIMENSION))
            Rrow = int(x % DIMENSION)
            (HORIZONTAL, VERTICAL) = self.convert_to_board_coordinates(Rrow, Rcol)
            if fen[Rcol][Rrow] == "p":
                self.screen.blit(self.BlackP, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "P":
                self.screen.blit(self.WhiteP, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "q":
                self.screen.blit(self.BlackQ, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "Q":
                self.screen.blit(self.WhiteQ, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "k":
                self.screen.blit(self.BlackK, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "K":
                self.screen.blit(self.WhiteK, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "r":
                self.screen.blit(self.BlackR, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "R":
                self.screen.blit(self.WhiteR, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "n":
                self.screen.blit(self.BlackN, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "N":
                self.screen.blit(self.WhiteN, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "b":
                self.screen.blit(self.BlackB, (HORIZONTAL,VERTICAL))
            elif fen[Rcol][Rrow] == "B":
                self.screen.blit(self.WhiteB, (HORIZONTAL,VERTICAL))
        
        def draw(self):
            self.drawBoard()
            fen = self.translate()
            self.draw_pieces(fen)
            p.display.update()

    def translate(self):
        return fenparser.FenParser(self.board.fen()).parse()

    def find_column(self, pos):
        return chess.square_file(self.FirstPosition)

    def find_row(self, pos):
        return chess.square_rank(self.FirstPosition)

    def GameState(self):
        if self.board.is_game_over() == True:
            if self.board.result() == "1-0":
                p.display.set_caption('White Has Won!')
            elif self.board.result() == "0-1":
                p.display.set_caption('Black Has Won')
            else:
                print("Game is drawn")
        
        p.quit()

    def main(self):
        p.event.set_blocked(p.MOUSEMOTION)
        self.draw()
        
        while True:
            if self.WTurn == True:
                p.display.set_caption("White")
                self.screen = p.display.set_mode((WIDTH,HEIGHT))
                self.player_move()
                
            else:
                self.screen = p.display.set_mode((WIDTH,HEIGHT))
                p.display.set_caption('AI Turn')
                self.board = evaluation.make_move(self.board) 
                self.turn = not self.WTurn
                self.draw()

    def pending_promotion(self):
        # we need to flip the Rrow to get the correct Rrow and columnvalues
        Rrow = 7 - self.find_row(self.FirstPosition)
        Rcol = self.find_column(self.FirstPosition)
        fen = self.translate()
        
        #this is determined by black or white pawn reaching the last Rrow
        if Rrow == 1 and fen[Rrow][Rcol] == "P":
            return True # white pawn reaching the end
        elif Rrow == 6 and fen[Rrow][Rcol] == "p":
            return True# black pawn reaching the end
        else: 
            return False

    def legalmovevalidation(self):
        if self.pending_promotion():
            #promote to a queen
            promo = chess.Move(from_square=self.FirstPosition, to_square=self.LastPosition, promotion=chess.QUEEN)
        else:    
            promo = chess.Move(from_square=self.FirstPosition, to_square=self.LastPosition)
        
        if promo in self.board.legal_moves:
            p.display.set_caption("Promoting")
            self.board.push(promo)
            self.Wturn = not self.WTurn
            self.GameState() 
        else:
            p.display.set_caption("not legal") # non legal moives will be ignored and displayed in the title
            return False

    def moves(self, sq):
        if self.LastPosition == None and self.FirstPosition != None:
            self.LastPosition = sq
            self.check_if_legal()
            self.FirstPosition = self.LastPosition = None
        if self.FirstPosition == None:
            self.FirstPosition = sq

    def player_moves(self):
        for event in p.event.get():
                if event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = p.mouse.get_pos()
                        square = self.ConvertToSquare(pos[0], pos[1])
                        self.move_piece(square)
                        self.draw()
                    
                if event.type == p.QUIT:
                        p.quit()
if __name__ == "__main__":
    c = CBoard()
    c.main()