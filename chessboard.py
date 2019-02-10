from ChessboardMotorController import MotorController
import RPi.GPIO as GPIO
import time


    
'''
    #Create the board and populate it with the standard chess setup
    #Uppercase - White
    #lowercase - Black
    #P- Pawn, R - Rook, H - Knight (Horse), B - Bishop, Q - Queen, K - King
    board = [['R','H','B','K','Q','B','H','R'], #1 0
             ['p','p','P','P','P','P','P','P'], #2 1
             [' ',' ',' ',' ',' ',' ',' ',' '], #3 2
             [' ',' ',' ',' ',' ',' ',' ',' '], #4 3
             [' ',' ',' ',' ',' ',' ',' ',' '], #5 4
             [' ',' ',' ',' ',' ',' ',' ',' '], #6 5
             ['p','p','p','p','p','p','p','p'], #7 6
             ['r','h','b','k','q','b','h','r']] #8 7
            #  H   G   F   E   D   C   B   A board
            #  0   1   2   3   4   5   8   7 array
'''


class Piece:
    #name - String that represents name of the piece
    #side - determine which side it belongs to (bool)
    name = "Space" #string
    color = 'N' #char Options W-white B-black N-neutral (tiles)
    
    #init makes an empty space. it can be populated or changed later
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
    #returns the name of the piece
    def getName(self):
        return self.name
    
    #returns the color of the piece
    def getColor(self):
        return self.color
    





class Board:
    cols = 8
    rows = 8
    #Begin board grid generation
    board = []
    verify = None
    
    
    def getPieceAt(self, row, col):
        return self.board[row][col]
    def setPieceAt(self, row, col, piece):
        self.board[row][col] = piece
    
    def __init__(self):
        for i in range(self.rows):
            # Create an empty list for each row
            self.board.append([])
            for j in range(self.cols):
                # Pad each column in each row with a 0
                self.board[i].append(Piece("Space", 'N'))
        #End board grid generation
        #self.verify = Verification(self)
    
    
    def defaultSetup(self):
        #Order of population: While back row, white pawns, black pawns, black back row
        #Set Rooks
        self.setPieceAt(0,0,Piece("Rook", 'W'))
        self.setPieceAt(0,7,Piece("Rook", 'W'))
        #Set Knights
        self.setPieceAt(0,1,Piece("Knight", 'W'))
        self.setPieceAt(0,6,Piece("Knight", 'W'))
        #Set Bishops
        self.setPieceAt(0,2,Piece("Bishop", 'W'))
        self.setPieceAt(0,5,Piece("Bishop", 'W'))
        #Set King & Queen
        self.setPieceAt(0,3,Piece("King", 'W'))
        self.setPieceAt(0,4,Piece("Queen", 'W'))
        
        #Pawns!
        for i in range(self.cols):
            self.setPieceAt(1, i, Piece("Pawn", 'W'))
            
        #Now for the black side
        #Set Rooks
        self.setPieceAt(7,0,Piece("Rook", 'B'))
        self.setPieceAt(7,7,Piece("Rook", 'B'))
        #Set Knights
        self.setPieceAt(7,1,Piece("Knight", 'B'))
        self.setPieceAt(7,6,Piece("Knight", 'B'))
        #Set Bishops
        self.setPieceAt(7,2,Piece("Bishop", 'B'))
        self.setPieceAt(7,5,Piece("Bishop", 'B'))
        #Set King & Queen
        self.setPieceAt(7,3,Piece("King", 'B'))
        self.setPieceAt(7,4,Piece("Queen", 'B'))
        #More pawns!
        for i in range(self.cols):
            self.setPieceAt(6, i, Piece("Pawn", 'B'))
    
    def verifyMove(self, beginRow, beginCol, endRow, endCol):
        #Check that the coordinates exist
        if(beginRow < 0 | beginRow > 7 | endRow < 0 | endRow > 7 ):
            return False
        if(beginCol < 0 | beginCol > 7 | endCol < 0 | endCol > 7 ):
            print("Invalid move @ verifyMove2")
            return False
        #Verify a movement is actually occuring
        if(beginRow == endRow & beginCol == endCol):
            
            print("Invalid move @ verifyMove3")
            return False
        
        #Check if a piece is actually present on the selected space
        if(self.getPieceAt(beginRow, beginCol).getColor() == 'N'):
            print("Invalid move @ verifyMove4")
            return False
        
        #Check if the piece at the given location can actually make the desired move
        if not (self.verifyPieceMove(self.getPieceAt(beginRow, beginCol), beginRow, beginCol, endRow, endCol)):
            print("Invalid move @ verifyMove5")
            return False
        
        #Verify that a player isn't capturing their own piece
        if(self.getPieceAt(beginRow,beginCol).getColor() == self.getPieceAt(endRow,endCol).getColor()):
            print("Invalid move @ verifyMove6")
            return False
        
        
        return True
    
    #Verify that it is possible for a given piece to move where it is being directed
    #Does not check if the destination is off of the board or if the destination is occupied (exception for pawns)
    #Does check for intervening pieces for all except Knight
    #NOTE: White starts on rows 0,1 and Black starts on rows 6,7
    def verifyPieceMove(self, piece, beginRow, beginCol, endRow, endCol):
        print(piece.getName())
        if(piece.getName() == "Pawn"):
            #White
            if(piece.getColor() == 'W'):
                #Pawns
                #Check if the pawn hasn't moved - if not, allow it to move forward 2 spaces
                if(beginRow == 1):
                    if((self.getPieceAt(beginRow+1,endCol).getColor() == 'N') & 
                       (self.getPieceAt(beginRow+2,beginCol).getColor() == 'N')):
                        return True
                #Check that the pawn is moving forward within its valid moveset
                if(endRow != beginRow + 1 | endCol < beginCol - 1 | endCol > beginCol + 1):
                    return False
                elif(beginCol == endCol & self.getPieceAt(endRow,endCol).getColor() != 'N'):
                    return False
                elif(beginCol != endCol & self.getPieceAt(endRow,endCol).getColor() != 'B'):
                    return False

            #Black
            elif(piece.getColor() == 'B'):
                t = 't'
                #Pawns
                #Check if the pawn hasn't moved - if not, allow it to move forward 2 spaces
                if(beginRow == 6):
                    if(self.board[beginRow - 1][beginCol].getColor() == 'N' & self.board[beginRow - 2][beginCol].getColor() == 'N'):
                        return True
                #Check that the pawn is moving forward within its valid moveset
                if(endRow != beginRow + 1 | endCol < beginCol - 1 | endCol > beginCol + 1):
                    return False
                elif(beginCol == endCol & self.board[endRow][endCol].getColor() != 'N'):
                    return False
                elif(beginCol != endCol & self.board[endRow][endCol].getColor() != 'W'):
                    return False
            return True
            
        #Knights
        #This is going to be ugly and I'm sorry for that
        #check for a straight line move
        elif(piece.getName() == "Knight"):
            if((beginRow == endRow) | (beginCol == endCol)):
                return False
            #Check for a diagonal move
            if(abs(endRow - beginRow) == abs(beginCol - endCol)):
                return False
            #Check if within valid knight parameters. I'm sorry for this
            if((((abs(endRow - beginRow) == 1) & (abs(beginCol - endCol) == 2)))| 
               (((abs(endRow - beginRow) == 2) & (abs(beginCol - endCol) == 1)))):
                return True
            print("fails @ Knight3")
            
        #Bishops
        elif(piece.getName() == "Bishop"):
            if((abs(beginRow - endRow) != abs(beginCol - endCol))):
                print(beginRow, endRow, beginCol, endCol)
                print("fails @ Bishop1")
                return False
            
            #This code is ugly. It only checks the spaces between the bishop's start and end position
            #It doesn't check who is occupying the destination space
            rowMultiplier = (endRow - beginRow)/(abs(endRow-beginRow))
            colMultiplier = (endCol - beginCol)/(abs(endCol-beginCol))
            
            #Check each intervening space
            for i in range(1, abs(endRow - beginRow)):
                if(self.getPieceAt(int(beginRow + (i*rowMultiplier)), int(beginCol + i*colMultiplier)).getColor() !='N'):
                    print("fails @ Bishop2")
                    return False
            return True
                    
        #Rooks
        elif(piece.getName() == "Rook"):
            if((beginRow != endRow) & (beginCol != endCol)):
                print("fails @ Rook1")
                return False
            
            #movement direction multiplier
            multiplier = 1
            #Check intervening spaces
            if(beginRow == endRow):
                multiplier = (endCol - beginCol)/(abs(endCol-beginCol))
                for i in range(1, abs(endCol - beginCol)):
                    if(board[endRow][beginCol+(i*multiplier)].getColor() != 'N'):
                        print("fails @ Rook2")
                        return False
            elif(beginCol == endCol):
                multiplier = (endRow - beginRow)/(abs(endRow-beginRow))
                for i in range(1, abs(endCol - beginCol)):
                    if(self.board[endRow+(i*multiplier)][beginCol].getColor() != 'N'):
                        print("fails @ Rook3")
                        return False
            return True
        #Queen
        elif(piece.getName() == "Queen"):
            if(self.verifyPieceMove(Piece("Rook", piece.getColor()), beginRow, beginCol, endRow, endCol)):
                return True
            elif(self.verifyPieceMove(Piece("Bishop", piece.getColor()), beginRow, beginCol, endRow, endCol)):
                return True
            else:
                return False
            
        #King
        elif(piece.getName() == "King"):
            if((abs(endRow - beginRow) > 1) | (abs(endCol - beginCol) > 1)):
                return False
            return True
        
    
    #Move a piece from its position to an new position
    def makeMove(self, beginRow, beginCol, endRow, endCol):
        valid = self.verifyMove(beginRow, beginCol, endRow, endCol)
        #if valid, check for capture then move
        if(valid):
            move = Move()
            if(self.getPieceAt(endRow, endCol).getColor() != 'N'):
                if(self.getPieceAt(endRow, endCol).getColor() != self.getPieceAt(beginRow, beginCol).getColor()):
                    #remove captured piece
                    move.capturePiece(endRow, endCol)
                    #update internal board 
                    self.setPieceAt(endRow, endCol, self.getPieceAt(beginRow, beginCol))
                    #Move the capturing piece
                    move.movePiece(beginRow, beginCol, endRow, endCol)
                    #update internal board
                    self.setPieceAt(beginRow, beginCol, Piece("Space", 'N'))
            else:
                #Move the piece on the board
                move.movePiece(beginRow, beginCol, endRow, endCol)
                #update internal board
                self.setPieceAt(endRow, endCol, self.getPieceAt(beginRow, beginCol))
                self.setPieceAt(beginRow, beginCol, Piece("Space", 'N'))
    
    '''
    def getBoardPosition(self):
    pos = chr(ord('H') - self.row)
    print(pos)
    pos += str(self.col + 1)
    return pos
    '''
        


# In[155]:


class Move:
    
    motorController = MotorController()

    
    #Remove piece at a position from the board
    def capturePiece(self, pieceRow, pieceCol):
        self.moveToPosition(pieceRow, pieceCol)
        self.grab()
        self.moveToGraveyard()
        self.release()
        
    #Move a piece from a start point to an end point    
    def movePiece(self, beginRow, beginCol, endRow, endCol):
        self.moveToPosition(beginRow, beginCol)
        self.grab()
        self.moveToPosition(beginRow, beginCol)
        self.release()
        
        
    def moveToPosition(self, position, isKnight):
        self.motorController.moveToPosition(position, isKnight)
    
    #Moves the given piece off the
    def moveToGraveyard(self):
        self.motorController.moveToGraveyard()
        
    #Activate the electromagnet
    def grab(self):
        self.motorController.grab()
        
    #Release the electromagnet
    def release(self):
        self.motorController.release()
    
    #Returns the motors to a known state
    def resetPosition():
        self.motorController.resetPosition()

class main:
   #String to store command
    #Command format: "[start letter][start number] [end letter][end number]
    command = "UNINITIALIZED"
    board = Board()
    def __init__(self):
        self.board.defaultSetup()
        self.controlLoop()
        
    
    #Parse a string command
    
    arr = [0, 0, 0, 0]
    
    def processCommand(self, commands):
        if(len(commands) == 4):
            counter = 7
            for i in range(len(commands)):
                if(i % 2 == 1):
                    if(commands[i] == '1'):
                        self.arr[i] = 0
                    elif(commands[i] == '2'):
                        self.arr[i] = 1
                    elif(commands[i] == '3'):
                        self.arr[i] = 2
                    elif(commands[i] == '4'):
                        self.arr[i] = 3
                    elif(commands[i] == '5'):
                        self.arr[i] = 4
                    elif(commands[i] == '6'):
                        self.arr[i] = 5
                    elif(commands[i] == '7'):
                        self.arr[i] = 6
                    elif(commands[i] == '8'):
                        self.arr[i] = 7
                elif(i % 2 == 0):
                    if(commands[i].upper() == 'A'):
                        self.arr[i] = 7
                    elif(commands[i].upper() == 'B'):
                        self.arr[i] = (6)
                    elif(commands[i].upper() == 'C'):
                        self.arr[i] = (5)
                    elif(commands[i].upper() == 'D'):
                        self.arr[i] = (4)
                    elif(commands[i].upper() == 'E'):
                        self.arr[i] = (3)
                    elif(commands[i].upper() == 'F'):
                        self.arr[i] = (2)
                    elif(commands[i].upper() == 'G'):
                        self.arr[i] = (1)
                    elif(commands[i].upper() == 'H'):
                        self.arr[i] = (0)
                    '''commands[i] = commands[i].upper()
                    t = ord(commands[i]) % 65
                    print("t = %", t)
                    for j in range(t):
                        counter -= 1
                    
                    self.arr[i] = (counter)
                    counter = 7'''
            print(self.arr)
            print(commands)
            self.board.makeMove(self.arr[1], self.arr[0], self.arr[3], self.arr[2])
    line = []      
    def controlLoop(self):
        usrIn = "NULL"
        while(usrIn != "q"):
            usrIn = input("Move (q to quit): ")
            coords = usrIn.split(' ')
            print(len(coords))
            if (len(coords) == 4):
                self.processCommand(coords)
            if(coords[0] == 'p'):
                for i in range(8):
                    self.line = []
                    for j in range(8):
                        self.line.append(self.board.getPieceAt(i,j).getColor())
                    print(self.line)
            
    
        
    
    '''
    print(board.getPieceAt(0,0).getName())
    #board.setPieceAt(0,0, Piece("Pawn", 'B'))
    board.defaultSetup()
    print(board.getPieceAt(0,0).getName())
    print(board.getPieceAt(0,0).getColor())
    print(board.getPieceAt(2,3).getName())
    print(board.getPieceAt(7,0).getColor())
    
    print(board.makeMove(1,0,3,0))
    print(board.getPieceAt(3,0).getName())
    '''
    #mqtt = MQTTConnection()
begin = main()
