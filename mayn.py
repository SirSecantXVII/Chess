import chess
#board creation and dimensions
import pygame as p
import math
#main file
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess game is 8x8
square_size = HEIGHT // DIMENSION
IMAGES = []


def main():
    p.init()
    



class CBoard():
    def __init__(self):
        self.board = chess.Board()
        p.init()
        self.screen = p.display.set_mode((WIDTH, HEIGHT))#
        clock = p.time.Clock()
        p.display.set_caption("Chess Engine")
        self.FPos = None
        self.LPos = None
        self.LoadImages()
        self.WTurn = 0

    
    def LoadImages(self):
        pieces = ["WhiteP", "BlackP", "WhiteN", "BlackN", "WhiteR", "BlackR", "WhiteK", "BlackK", "WhiteQ", "BlackQ", "WhiteB", "BlackB"]
        for piece in pieces:
            IMAGES[piece] = p.transform.scale(p.image.load("pieceimages/" + piece + ".png"), (square_size, square_size))

if __name__ == "__main__":
    main()