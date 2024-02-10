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
BLUE = (0, 0, 255)
GREEN = (0,255,0)
RED = (255,0,0)

# Define piece class
class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.immovable = False
        self.highlighted = False
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, PIECE_SIZE, PIECE_SIZE)

    def snap_to_grid(self,x,y):
        self.x = math.floor(x / CELL_SIZE) * CELL_SIZE
        self.y = math.floor(y / CELL_SIZE) * CELL_SIZE
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if self.highlighted == True:
            pygame.draw.rect(screen, BLACK, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
class BigPiece():
    def __init__(self, shape):
        self.shape = shape
        self.color = BLUE
        self.pieces = []
        self.clickedPiece = None
        self.construct()
    def rotate(self):
        self.shape = np.rot90(self.shape)
        self.construct()
    def construct(self):
        self.pieces = []
        for i in range(len(self.shape)):
            row = []
            for j in range(len(self.shape[i])):
                if (self.shape[i][j]==1):
                    piece = Piece(j*CELL_SIZE, i*CELL_SIZE, self.color)
                    row.append(piece)
            self.pieces.append(row)
    def highlight(self, t):
        for row in self.pieces:
            for piece in row:
                piece.highlighted=t
    
    def draw(self, screen):
        for row in self.pieces:
            for piece in row:
                piece.draw(screen)

    def checkClicked(self,x,y):
        for row in self.pieces:
            for piece in row:
                if (piece.x <=x and (piece.x+PIECE_SIZE)>=x and piece.y <=y and (piece.y+PIECE_SIZE)>=y): 
                    self.highlight(True)
                    self.clickedPiece = piece
                    return True
        return False

    def translate(self, rows, cols):
        for row in self.pieces:
            for piece in row:
                piece.y += rows * CELL_SIZE
                piece.x += cols * CELL_SIZE
                piece.rect.topleft = (piece.x, piece.y)

    
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
                        [0,1,1]]))
corner_piece = BigPiece(np.array([[1,0,0],
                                [1,0,0],
                                [1,1,1]]))
blockpiece = BigPiece(np.array([[1,1,1],
                            [1,1,1]]))
upiece = BigPiece( np.array([[1,0,1],
                        [1,1,1]]))
pinkpiece = BigPiece(np.array([[1,1,0],
                            [1,1,1]]))
lpiece = BigPiece(np.array([[1,0],
                        [1,0],
                        [1,0],
                        [1,1]]))
ypiece = BigPiece(np.array([[1,0],
                        [1,1],
                        [1,0],
                        [1,0]]))
zzpiece = BigPiece(np.array([[1,0],
                        [1,0],
                        [1,1],
                        [0,1]]))
pieces = []
pieces.append(zpiece)
cpiece = -1
board = Board()
# Main loop
running = True
display = [["Jan", "Feb", "Mar", "Apr", "May", "Jun"],["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],[1,2,3,4,5,6,7],[8,9,10,11,12,13,14], [15,16,17,18,19,20,21], [22,23,24,25,26,27,28], [29,30,31]]     
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('yay')
                if(cpiece>-1):
                    clicked = pieces[cpiece]
                    clicked.rotate()
                    clicked.highlight(False)
                    cpiece = -1

        # Handle mouse click to create new pieces
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x,y)
            if (cpiece>-1):
                clicked = pieces[cpiece] 
                cols = math.floor(x / CELL_SIZE)-(clicked.clickedPiece.x/CELL_SIZE)
                rows = math.floor(y / CELL_SIZE)-(clicked.clickedPiece.y/CELL_SIZE)
                clicked.translate(rows,cols)
                clicked.highlight(False)
                cpiece = -1
            else:
                for i in range(len(pieces)):
                    if(piece.checkClicked(x,y)): 
                        cpiece = i



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
