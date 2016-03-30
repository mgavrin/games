import random

class Board:
    def __init__(self,height,width,percentBombs):
        self.height=height
        self.width=width
        self.boardArray=[]
        self.bombsRemaining=0
        self.displayBombsRemaining=0
        #create array of bombs
        for y in range(0,self.height):
            thisRow=[]
            for x in range(0,self.width):
                bombRoll=random.randint(0,99)
                if bombRoll<percentBombs:
                    thisRow.append(Square("b",x,y,self))
                    self.bombsRemaining+=1
                    self.displayBombsRemaining+=1
                else:
                    thisRow.append(Square("clear",x,y,self))
            self.boardArray.append(list(thisRow))
            
        #get adjacent squares and set bomb counts
        for y in range(0,self.height):
            for x in range(0,self.width):                
                tempSquare=self.getSquare(x,y)
                tempSquare.setAdjacentSquares()
                tempSquare.setNumBombs()


    def inBoard(self,x,y):
        #returns true if x,y is a valid square
        return(x>=0 and y>=0 and x<self.width and y<self.height)

    def getSquare(self,x,y):
        #returns the Square instance at given coordinates if it exists
        if self.inBoard(x,y):
            return self.boardArray[y][x]

    def __repr__(self):
        output=""
        for row in self.boardArray:
            output+=repr(row)
            output+="\n"
        return output

    def __str__(self):
        return repr(self)

class Square:
    def __init__(self,value,x,y,board):
        self.value=value
        #allowable states: ints 0-8, "b"
        self.displayState="u"
        #allowable states: "u" (untouched, "d" (dug), "f" (flagged)
        self.x=x
        self.y=y
        self.board=board

    def setAdjacentSquares(self):
        self.adjacentSquares=[]
        #returns a list of squares adjacent to self
        for xOffset in range(-1,2):
            for yOffset in range(-1,2):
                newX=self.x+xOffset
                newY=self.y+yOffset
                if self.board.inBoard(newX,newY):
                    self.adjacentSquares.append(self.board.getSquare(newX,newY))

    def setNumBombs(self):
        #counts and sets the number of bombs adjacent to a square
        if self.value!="b":
            numBombs=0
            for Square in self.adjacentSquares:
                if Square.value=="b":
                    numBombs+=1
            self.value=numBombs

    def __str__(self):
        return str(self.value)+self.displayState

    def __repr__(self):
        return str(self.value)+self.displayState

    def flag(self):
        #toggles flaggedness of square
        if self.displayState=="u":
            self.displayState="f"
            self.board.displayBombsRemaining-=1
            if self.value=="b":
                self.board.bombsRemaining-=1
        elif self.displayState=="f":
            self.board.displayBombsRemaining+=1
            self.displayState="u"
            if self.value=="b":
                self.board.bombsRemaining+=1

    def dig(self):
        if self.displayState=="u":
            if self.value=="b":
                raise ValueError("BOOM YOU DIED")
            elif self.value>0:
                self.displayState="d"
            else:
                self.displayState="d"
                for Square in self.adjacentSquares:
                    if Square.displayState=="u":
                        Square.dig() #recursion!
            

###########Inits of stuff###########
testBoard=Board(10,10,20)
