import numpy as np
import time
class Board():
    @staticmethod
    def getBoardPos(month, day):
        indicies=[(0,0),(0,0)]
        if month>5:
            indicies[0] = (1,month-7)
        else:
            indicies[0] =  (0,month-1)
        indicies[1] =(int(day/7 + 2), day % 7-1)
        return indicies
    
    def initalBoard(month,day):
        board = np.zeros((7,7))
        board[0:2,6] = np.ones(2)
        board[6,3:7] = np.ones(4)
        indicies = Board.getBoardPos(month,day)
        row_d, col_d = indicies[1]
        row_m, col_m = indicies[0]
        board[row_d][col_d]=1
        board[row_m][col_m]=1
        return board
    
    def __init__(self, month,day):
        self.current_layout = Board.initalBoard(month, day)
        self.recursion = []
        self.solutions = []
        self.recursion.append(np.copy(self.current_layout))
        self.index = 0
        self.pieces = []
    
    
    def displayBoard(self):
        display = [["Jan", "Feb", "Mar", "Apr", "May", "Jun"],["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],[1,2,3,4,5,6,7],[8,9,10,11,12,13,14], [15,16,17,18,19,20,21], [22,23,24,25,26,27,28], [29,30,31]]
        for i in range(len(display)):
            row = "|"
            for j in range(len(display[i])):
                spot = display[i][j]
                if self.current_layout[i][j]>0:
                    spot = " ~ "
                if type(spot) is int: 
                    row+= ' '
                    if spot<10:
                        row+=' '
                row+= ' '+str(spot)+' |'
            print(row)
        
    
    def isValidPos(self, board):
        if (2 in board):
            return False
        return not self.checkIsolated(board)
    
    def solve(self,index):
        piece = self.pieces[index]
        self.recursion.append(np.copy(self.current_layout))
        for i in range(piece.getRotations()):
            piece.rotate()
            length, width = piece.shape()
            for j in range(8 - width):
                for k in range(8- length):
                    if(self.placePieceOnBoard(piece, k,j)):
                        if (self.isSolved()):
                            print("yay")
                            self.solutions.append (np.copy(self.recursion))
                        else: 
                            self.solve(index+1)
        self.recursion.pop()
        self.current_layout = np.copy(self.recursion[-1])
        

                        
           
    def isSolved(self):
        if 0 in self.current_layout:
            return False
        return True
    

    def checkNeighbors(self, board, row, col):
        neighbors = []
        left= [row, col-1]
        right =[row, col+1]
        up = [row-1, col]
        down = [row+1, col]
        if row>0:
            neighbors.append(board[up[0]][up[1]])
        if col>0:
           neighbors.append(board[left[0]][left[1]])
        if row<len(board)-1:
            neighbors.append(board[down[0]][down[1]])
        if col<len(board[row])-1:
            neighbors.append(board[right[0]][right[1]])
        return not 0 in neighbors 
    

        
    def checkIsolated(self,board):
        length, width = board.shape
        for row in range(length):
            for col in range(width):
                if(board[row][col] == 0 and self.checkNeighbors(board,row,col)):
                    return True
        return False
                    

        
    def setPieces(self, pieces):
        self.pieces = pieces


    def placePieceOnBoard(self, piece, row, col):
        board = np.copy(self.current_layout)
        rows, cols = piece.shape()
        endrow = (rows+row)
        endcol = cols+col
        board[row:endrow, col:endcol] += piece.getArray()
        if (self.isValidPos(board)):
            self.current_layout[row:endrow, col:endcol] += piece.getArray()
            return True
        else:
            return False
        

        

class Piece():
    def __init__(self,piece, rot=4):
        self.piece = piece
        self.rotations = rot

    def rotate(self):
        self.piece = np.rot90(self.piece)
    def shape(self):
        return self.piece.shape
    def getArray(self):
        return (self.piece)
    def getRotations(self):
        return self.rotations
        

zpiece = Piece(np.array([[1,1,0],
                        [0,1,0],
                        [0,1,1]]),2)
corner_piece = Piece(np.array([[1,0,0],
                                [1,0,0],
                                [1,1,1]]))
blockpiece = Piece(np.array([[1,1,1],
                            [1,1,1]]),2)
upiece = Piece( np.array([[1,0,1],
                        [1,1,1]]))
pinkpiece = Piece(np.array([[1,1,0],
                            [1,1,1]]))
lpiece = Piece(np.array([[1,0],
                        [1,0],
                        [1,0],
                        [1,1]]))
ypiece = Piece(np.array([[1,0],
                        [1,1],
                        [1,0],
                        [1,0]]))
zzpiece = Piece(np.array([[1,0],
                        [1,0],
                        [1,1],
                        [0,1]]))
board = Board(2,10)
board.displayBoard()
board.setPieces([zpiece, corner_piece, blockpiece,upiece,pinkpiece,lpiece,ypiece,zzpiece])
start = time.time()
print(board.solve(0))
print(board.solutions)
end = time.time()
print(end-start)