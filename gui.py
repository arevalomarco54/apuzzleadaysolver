import pygame
import math
import numpy as np
# Define grid dimensions
CELL_SIZE =60
BLANK_SQUARES = 2
WHITE_SPACE = CELL_SIZE*BLANK_SQUARES
GRID_WIDTH = CELL_SIZE *7+2*WHITE_SPACE
GRID_HEIGHT = CELL_SIZE *7+2*WHITE_SPACE

# Define piece size
PIECE_SIZE = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption("A Puzzle a Day")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34,171,36)
PURPLE = (109,59,191)
YELLOW = (191,194,18)
MAGENTA = (205,14,102)
BLUE = (15, 130, 242)
PINK = (230,135,179)
ORANGE = (253,140,0)
GREY = (119,119,119)

# Define piece class
class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.row = 0
        self.col = 0
        self.immovable = False
        self.highlighted = False
        self.color = color
        self.r,self.g,self.b = color
        self.rect = pygame.Rect(self.x, self.y, PIECE_SIZE, PIECE_SIZE)
    
    #Draw piece on board
    def draw(self, screen):
        if self.highlighted == True:
            pygame.draw.rect(screen, (self.r/1.3,self.g/1.3,self.b/1.3), self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x+CELL_SIZE, self.y ), 1)
        pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x, self.y+CELL_SIZE ), 1)
        pygame.draw.line(screen, BLACK, (self.x+CELL_SIZE, self.y), (self.x+CELL_SIZE, self.y+CELL_SIZE ), 1)
        pygame.draw.line(screen, BLACK, (self.x, self.y+CELL_SIZE), (self.x+CELL_SIZE, self.y+CELL_SIZE), 1)
        
    #Translate piece by a set amount of rows and cols
    def translate(self, rows, cols):
        self.position(self.x + cols * CELL_SIZE, self.y + rows*CELL_SIZE)
        
    #Place piece at a given x and y value
    def position(self, x ,y):
        self.y = y
        self.x = x
        self.rect.topleft = (self.x, self.y)
        self.row = self.y/CELL_SIZE
        self.col = self.x/CELL_SIZE


#Define a BigPiece class
#A BigPiece is an array of Piece classes in a given shape
class BigPiece():
    #initialize class with shape
    def __init__(self, shape, color=BLUE,pos = (0,0),):
        self.shape = shape
        self.color = color
        self.row, self.col = pos
        self.pieces = []
        self.clickedPiece = None
        self.construct()
    
    #Rotate the shape of the pieces and reposition piece
    def rotate(self, times):
        self.pieces = np.rot90(self.pieces, times)
        for i in range(len(self.pieces)):
            for j in range(len(self.pieces[i])):
                if (not self.pieces[i][j]==0):
                    piece = self.pieces[i][j]
                    piece.position((j+self.col)*CELL_SIZE, (i+self.row)*CELL_SIZE )

    
    #Construct piece based on given array
    def construct(self):
        del self.pieces
        self.pieces = []
        for i in range(len(self.shape)):
            row = []
            for j in range(len(self.shape[i])):
                if (self.shape[i][j]==1):
                    piece = Piece((j+self.col)*CELL_SIZE, (i+self.row)*CELL_SIZE, self.color)
                    row.append(piece)
                else:
                    row.append(0)
            self.pieces.append(row)
        self.pieces = np.array(self.pieces)
    
    #Highlight a BigPiece, or unhighlight it
    def highlight(self, t):
        for row in self.pieces:
            for piece in row:
                if not piece ==0:
                    piece.highlighted=t
    
    #Draw BigPiece to board by drawing each of the Piece in the array
    def draw(self, screen):
        for row in self.pieces:
            for piece in row:
                if not piece ==0:
                    piece.draw(screen)

    #Check to see if BigPiece has been clicked by checking to see if any Piece has been clicked
    def checkClicked(self,x,y):
        for row in self.pieces:
            for piece in row:
                if (not piece ==0 and piece.x <=x and (piece.x+PIECE_SIZE)>=x and piece.y <=y and (piece.y+PIECE_SIZE)>=y): 
                    self.highlight(True)
                    self.clickedPiece = piece
                    return True
        return False
    
    #Translate BigPiece to a given x,y coordinate
    def translate(self, x, y):
        cols = math.floor(x / CELL_SIZE)-(self.clickedPiece.x/CELL_SIZE)
        rows = math.floor(y / CELL_SIZE)-(self.clickedPiece.y/CELL_SIZE)
        minrow = 100
        mincol =100
        for row in self.pieces:
            for piece in row:
                if not piece ==0:
                    piece.translate(rows, cols)
                    if piece.row<minrow:
                        minrow = piece.row
                    if piece.col <mincol:
                        mincol = piece.col
        self.row = minrow
        self.col = mincol


    
#define Board class
class Board():
    def __init__(self):
        self.font = pygame.font.SysFont('Times New Roman', int(CELL_SIZE/2))
    
    #Draw grid
    def drawGrid(self):
        for i in range(WHITE_SPACE, GRID_WIDTH+1-WHITE_SPACE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (i, WHITE_SPACE), (i, GRID_HEIGHT-WHITE_SPACE), 1)
        for i in range(WHITE_SPACE, GRID_HEIGHT+1-WHITE_SPACE, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (WHITE_SPACE, i), (GRID_WIDTH-WHITE_SPACE, i), 1)
    
    #Draw text labels
    def drawLabels(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                screen.blit(self.font.render(str(board[i][j]), True, BLACK), (WHITE_SPACE+j*CELL_SIZE, WHITE_SPACE+CELL_SIZE/4+i*CELL_SIZE))

# Create a list of pieces
zpiece = BigPiece(np.array([[1,1,0],
                        [0,1,0],
                        [0,1,1]]),GREEN,(4,0))
corner_piece = BigPiece(np.array([[1,0,0],
                                [1,0,0],
                                [1,1,1]]),YELLOW, (6,0))
blockpiece = BigPiece(np.array([[1,1,1],
                            [1,1,1]]), BLUE,(9,9))
upiece = BigPiece( np.array([[1,0,1],
                        [1,1,1]]),GREY, (0,9))
pinkpiece = BigPiece(np.array([[1,1,0],
                            [1,1,1]]), PINK, (6,9))
lpiece = BigPiece(np.array([[1,0],
                        [1,0],
                        [1,0],
                        [1,1]]), ORANGE, (3,9))
ypiece = BigPiece(np.array([[1,0],
                        [1,1],
                        [1,0],
                        [1,0]]), MAGENTA, (9,3))
zzpiece = BigPiece(np.array([[1,0],
                        [1,0],
                        [1,1],
                        [0,1]]), PURPLE, (0,0))


pieces = [zpiece, corner_piece, blockpiece,upiece,pinkpiece,lpiece,ypiece,zzpiece]
board = Board()


# Main loop
running = True
clicked =False
display = [["Jan", "Feb", "Mar", "Apr", "May", "Jun"],["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],[1,2,3,4,5,6,7],[8,9,10,11,12,13,14], [15,16,17,18,19,20,21], [22,23,24,25,26,27,28], [29,30,31]]     
while running:
    for event in pygame.event.get():
        #Quite game
        if event.type == pygame.QUIT:
            running = False

        #Rotate piece based on arrow
        if event.type == pygame.KEYDOWN:
            if(clicked):
                clicked_piece = pieces[-1]
                if event.key == pygame.K_LEFT:
                    clicked_piece.rotate(1)
                    
                if event.key == pygame.K_RIGHT:
                    clicked_piece.rotate(3)
    
                

        # If mouse is pressed, bring piece to top layer, highlight, and put clicked as true
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i in range(len(pieces)-1,-1,-1):
                piece= pieces[i]
                if(piece.checkClicked(x,y)): 
                    pieces.append( piece)
                    pieces.remove(piece)
                    clicked = True
                    break
        
        #Once mouse is let go, disable clicked, and unhighlight
        if event.type == pygame.MOUSEBUTTONUP:
            clicked_piece = pieces[-1] 
            clicked_piece.highlight(False)
            clicked = False
    
    #Move piece on top layer based on mouse
    if clicked:
        x, y = pygame.mouse.get_pos()
        clicked_piece = pieces[-1] 
        clicked_piece.translate(x,y)



    # Fill screen with white
    screen.fill(WHITE)

    # Draw grid lines
    board.drawGrid()

    board.drawLabels(display)
    # Draw pieces
    for piece in pieces:
        piece.draw(screen)
    

    pygame.display.update()

pygame.quit()
