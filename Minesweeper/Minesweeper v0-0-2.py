import random
import pygame
from pygame import *
import sys #for quitting the game
from collections import deque


class Board:
    def __init__(self,height,width,percentBombs):
        self.clock=pygame.time.Clock()
        pygame.time.set_timer(6,milsBetweenMoves)
        self.height=height
        self.width=width
        self.boardArray=[]
        self.squares=[]
        self.size=(pixel*width+border*2, pixel*height+border+topBorder)
        self.screen= pygame.display.set_mode(self.size, 0, 32)
        self.movesToDo=deque([]) #Empty move queue
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

    def getAutoMoves(self):#GLaDOS was here
        #returns a list of AI-generated moves to be added to the move queue
        self.movesToDo=deque([])#erase old moves
        for Square in self.squares:
                moves=Square.getMoveList()
                self.movesToDo.extend(moves)        

    def updateScreen(self):
        self.screen.fill(background_color) #fill with background color
        #Get each square on the board, request its image
        #and draw it to the screen at the appropriate position
        textImg=mainFont.render("Bombs Remaining: "+str(self.displayBombsRemaining),False,threeRed)
        self.screen.blit(textImg,(border,topBorder/2))
        for x in range(0,self.width):
            for y in range(0,self.height):
                tmpSquare=self.getSquare(x,y)
                tmpImage=tmpSquare.getImage()
                xPos=border+x*pixel
                yPos=topBorder+y*pixel
                self.screen.blit(tmpImage, (xPos,yPos))

        #last, flip the screen to show this all
        pygame.display.flip()

    def inBoard(self,pos,y="bananas"):
        #returns true if x,y is a valid square
        if y=="bananas": #got a tuple
            x=pos[0]
            y=pos[1]
        else: #got two numbers
            x=pos
        return(x>=0 and y>=0 and x<self.width and y<self.height)

    def getSquare(self,pos,y="bananas"):
        #returns the Square instance at given coordinates if it exists, given whatever method of pointing at it you like
        if y=="bananas": #got a tuple
            x=pos[0]
            y=pos[1]
        else: #got two numbers
            x=pos
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

    def findClick(self,pos,y="bananas"):
        #finds which x and y in squares was clicked given x and y in pixels, either as 2 numbers or as a tuple thereof
        if y=="bananas": #got a tuple
            x=pos[0]
            y=pos[1]
        else: #got two numbers
            x=pos
        outY=(y-topBorder)/pixel
        outX=(x-border)/pixel
        return outX,outY

    def mainloop(self):
        ####ye mainloope
        while True:
            events=pygame.event.get()
            for event in events:
                if event.type==6:
                    try:
                        move=self.movesToDo.popleft()#gets the oldest move from the AI's move queue
                        move()
                    except:
                        print "AI is stumped. Please help."
                if event.type==QUIT:
                    pygame.display.quit()
                    sys.exit()
                if event.type==MOUSEBUTTONDOWN:
                    pos=event.pos #location of click in pixels
                    button=event.button #left click or right click
                    clickedSquare=self.findClick(pos)
                    self.processUserClick(button,clickedSquare)
            
            for square in self.squares:
                square.update()
            if self.displayBombsRemaining==0 and self.bombsRemaining==0:
                print "You and the AI just won!"
                pygame.display.quit()
                sys.exit()
            self.getAutoMoves()
            self.updateScreen()
            

    def processUserClick(self,button,square):
        #handles a click of a button on a square
        #button 1 is left click, button 3 is right click, button 2 and 4+ is shenanigans
        if self.inBoard(square):
            square=self.getSquare(square)#what have I done/ultimate navel gaze/it's squares all the way down
            if button==1:
                square.dig()
            elif button==3:
                if square.displayState=="f":
                    square.deflag()
                elif square.displayState=="u":
                    square.flag()

##    def getBestGuess(self):
##        odds=[]
##        for square in self.squares:
##            odds.append(square,square.guessOdds())
##        #find square with lowest odds of being a bomb
##        lowestOdds=1.1
##        currentBestSquare=squares[0]
##        for option in odds:
##            if option[1]<lowestOdds:
##                currentBestSquare=option[0]
##                lowestOdds=option[1]
##        return currentBestSquare
                
            

class Square:
    def __init__(self,value,x,y,board):
        self.value=value
        #allowable states: ints 0-8, "b"
        self.displayState="u"
        #allowable states: "u" (untouched, "d" (dug), "f" (flagged)
        self.x=x
        self.y=y
        self.isSafe=False #True if the AI knows the square is not a bomb
        self.board=board
        self.board.squares.append(self)

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
        #flags a square
        if self.displayState=="u":
            self.displayState="f"
            self.board.displayBombsRemaining-=1
            if self.value=="b":
                self.board.bombsRemaining-=1

    def deflag(self):#helper function for puny humans
        #deflags a square
        if self.displayState=="f":
            self.board.displayBombsRemaining+=1
            self.displayState="u"
            if self.value=="b":
                self.board.bombsRemaining+=1

    def dig(self):
        if self.displayState=="u":
            if self.value=="b":
                print "BOOM YOU DIED"
                pygame.display.quit()
                sys.exit()
            elif self.value>0:
                self.displayState="d"
            else:
                self.displayState="d"
                for Square in self.adjacentSquares:
                    if Square.displayState=="u":
                        Square.dig() #recursion!
    def getImage(self):
        #returns a pygame surface object ready for blitting based on local variables self.value and self.displayState
        baseImage=pygame.Surface((pixel,pixel)) #Create a base the size of one square
        
        #Fill baseImage with appropriate colors (set in inits at the very bottom)
        if self.displayState=="u":
            baseImage.fill((undug_color))
        elif self.displayState=="f":
            baseImage.fill((flagged_color))
        elif self.displayState=="d":
            baseImage.fill((dug_color))
        
        #Draw on the appropriate text, if any
        if self.displayState=="d":
            charImg=mainFont.render(str(self.value), False, colorDict[self.value])
        elif self.displayState=="f":
            charImg=mainFont.render("F", False, colorDict["F"])
        else:
            charImg=False
        if charImg:
            size=charImg.get_rect()
            xPos=(pixel-size.width)/2
            yPos=(pixel-size.height)/2
            baseImage.blit(charImg,(xPos,yPos+2))

        #Draw border lines
        pygame.draw.rect(baseImage, line_color, baseImage.get_rect(),1)
        
        #Return baseImage
        return baseImage

    def update(self):
        #Updates all adjacency lists, bomb counts, and square's clear and safe status

        self.numBombsFlagged=0
        self.undugAdjacents=[]
        self.dugAdjacents=[]
        
        for Square in self.adjacentSquares:
            #Recount the number of tangent player-flagged squares
            if Square.displayState=="f":
                self.numBombsFlagged+=1
            #Add undug squares to a list
            if Square.displayState=="u":
                self.undugAdjacents.append(Square)
            if Square.displayState=="d":
                self.dugAdjacents.append(Square)
        #Remaining bombs is the difference of flagged bombs and tangent bombs
        if self.value!="b":
            self.numBombsRemaining = self.value - self.numBombsFlagged
        else:
            self.numBombsRemaining=99

        #Check if this square is now clear
        if self.displayState=="d" and self.numBombsRemaining<=0 :
            self.isClear=True
            if self.value=="b":
                print "GLaDOS fucked up if this is showing."
        else:
            self.isClear=False

        
                    
                

    def getMoveList(self):#GLaDOS was here
        moveList=[]
        #take this out in a minute
        if self.isSafe and self.displayState=="u":
            moveList.append(self.dig)

        #If all the bombs near a square are accounted for, dig the rest of the adjacent squares
        if self.isClear:
            for Square in self.undugAdjacents:
                moveList.append(Square.dig)
                
        #If a square only sees n squares and sees n bombs, THEY'RE ALL MINES!
        elif self.numBombsRemaining==len(self.undugAdjacents):
            for Square in self.undugAdjacents:
                moveList.append(Square.flag)

        #deductive as heck:
        #if one square sees all the bombs another sees,
        #then any squares the first square doesn't see and the second does are safe
        #AND if one square sees all the safe spaces another sees,
        #the ones left are bombs
        for Square in self.dugAdjacents:
            if isSubset(self.undugAdjacents,Square.undugAdjacents):
                #other square "Square" sees all the undug squares self does, and possibly some others
                remainingBombs=Square.numBombsRemaining-self.numBombsRemaining
                #The number of bombs the other square sees that we don't
                remainder=getRemainder(self.undugAdjacents,Square.undugAdjacents)
                #list of squares which other square sees and self doesn't
                if remainingBombs==0:
                    for square in remainder:
                        moveList.append(square.dig)
                if remainingBombs==len(remainder):
                    for square in remainder:
                        moveList.append(square.flag)
        return moveList

def isSubset(a,b):
    #returns True iff a is a subset of b
    for elem in a:
        if elem not in b:
            return False
    return True

def getRemainder(a,b):
    if isSubset(a,b):
        remainder=[]
        for elem in b:
            if elem not in a:
                remainder.append(elem)
        return remainder
    else:
        return []

###########Inits of stuff###########

#startup pygame
pygame.init()

pixel=25
topBorder=100
border=50
fontBorder=3
fontHeight=pixel-2*fontBorder
frameRate=3
milsBetweenMoves=1000/frameRate

#Color inits
undug_color=pygame.Color(180,180,180)
dug_color=pygame.Color(220,220,220)
background_color=pygame.Color(240,240,240)
line_color=pygame.Color(0,0,0)
flagged_color=undug_color
green=pygame.Color(0,255,0)
red=pygame.Color(255,0,0)
blue=pygame.Color(0,0,255)

oneBlue=pygame.Color(65,115,170)
twoGreen=pygame.Color(80,135,55)
threeRed=pygame.Color(235,40,40)
tooManyBombsGray=pygame.Color(90,90,90)

colorDict={0:dug_color, 1:oneBlue, 2:twoGreen, 3:threeRed, 4: tooManyBombsGray,
           5: tooManyBombsGray, 6:tooManyBombsGray, 7:tooManyBombsGray, 8:tooManyBombsGray, "F":red, "b":red}

mainFont=pygame.font.SysFont("courier new",fontHeight)
mainFont.set_bold(True)

testBoard=Board(75,75,20)
testBoard.mainloop()
