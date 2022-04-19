from ChessE import *
import pygame as p
#main file
p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess game is 8x8
square_size = HEIGHT // DIMENSION
max_FPS = 15 #slide animations
IMAGES = {}

#Creation of a Dictionary to link images
def LoadImages():
    pieces = ["wp", "bp", "wN", "bN", "wR", "bR", "wK", "bK", "wQ", "bQ", "wB", "bB"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("pieceimages/" + piece + ".png"), (square_size, square_size))
        # this iterates through all the pieces to load them into the dictionary now we can call an images by "IMAGES["wp"]"

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gamestate = State()
    LoadImages()
    run = True
    selectedsquare = ()#tuple
    playerClick = []#keeps track of player clicks also a tuple
    while run:
        for x in p.event.get():
            if x.type == p.QUIT:
                run = False #Closes game
            elif x.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos() #this gets the x and y locations of the mouse cursor when it is clicked
                col = loc[0]//square_size
                row = loc[1]//square_size
                if selectedsquare == (row,col): # user clicks same square twice
                    selectedsquare = () #clears tuple meaning deselcts
                    playerClick = [] #clear player clicks
                else:
                    selectedsquare = (row,col)
                    playerClick.append(selectedsquare) # appends both clicks
                    if len(playerClick) == 2: #after 2nd click
                        move = Move(playerClick[0], playerClick[1], gamestate.board)
                        print(move.GetChessNotat())
                        gamestate.makeMove(move)
                        selectedsquare = ()
                        playerClick = []
            #undo key
            elif x.type == p.KEYDOWN:
                if x.key == p.K_r: #THIS UNDOS WHEN "r" is pressed
                    gamestate.undoMove()
        drawState(screen, gamestate)
        clock.tick(max_FPS)
        p.display.flip()

#This function is responsible in a game state

def drawState(screen,gs):
    drawBoard(screen) #draw squares on the board
    #add in piece highlighting or move suggestions(later)
    drawPieces(screen, gs.board) # draws pieces ontop of squares

#draw the squares on the board. The top left square is always light.

def drawBoard(screen):
    colours = [p.Color("white"), p.Color("brown")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colours[((row+col) % 2)]#alternating
            p.draw.rect(screen, color, p.Rect(col*square_size, row*square_size, square_size, square_size)) 
#Draw the pieces on the using the current  State board
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "xx": # not an empty square
               screen.blit(IMAGES[piece], p.Rect(col*square_size, row*square_size, square_size, square_size))

if __name__ == "__main__":
    main()