import pygame
import math
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

class big
# Create a list of pieces
pieces = [Piece(0, 0, BLUE)]
cpiece = -1
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle mouse click to create new pieces
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x,y)
            if (cpiece>-1):
                print()
                pieces[cpiece].snap_to_grid(x,y)
                piece.highlighted=False
                cpiece = -1
            else:
                for i in range(len(pieces)):
                    piece = pieces[i]
                    print(piece.x, piece.y)
                    if (piece.x <=x and (piece.x+PIECE_SIZE)>=x and piece.y <=y and (piece.y+PIECE_SIZE)>=y): 
                        cpiece = i
                        piece.highlighted=True


    # Fill screen with white
    screen.fill(WHITE)

    # Draw grid lines
    for i in range(WHITE_SPACE, GRID_WIDTH+1-WHITE_SPACE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (i, WHITE_SPACE), (i, GRID_HEIGHT-WHITE_SPACE), 1)
    for i in range(WHITE_SPACE, GRID_HEIGHT+1-WHITE_SPACE, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (WHITE_SPACE, i), (GRID_WIDTH-WHITE_SPACE, i), 1)

    # Draw pieces
    for piece in pieces:
        piece.draw(screen)

    pygame.display.flip()

pygame.quit()
