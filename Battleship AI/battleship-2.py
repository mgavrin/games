import pygame
from pygame.locals import *
import random
from random import *
import math
from math import *

pygame.init()

class Grid:
    def __init__(self,location,name,dim,game):
        #Unpack location into x and y co-ordinates of upper left corner
        self.base_x=location[0]
        self.base_y=location[1]
        self.dim=dim
        self.name=name
        self.game=game
        self.game.boards.append(self)
        self.lines=self.game.lines
        #and now to creat the board state memory
        #The goal of this code is to create a boad of dimensions dim by dim
        # The end result below would result with dim=3
        #    [ [0,0,0]
        #      [0,0,0]
        #      [0,0,0] ]temp=0
        self.board=[]
        temp=0
        while temp<dim:
            tmp=0
            row=[]
            while tmp<dim:
                row.append(0)
                tmp+=1
            self.board.append(row)
            temp+=1

        #Create a temporary state matrix that can be modified without changing permanent matrix
        self.tempBoard=[]
        temp=0
        while temp<dim:
            tmp=0
            row=[]
            while tmp<dim:
                row.append(0)
                tmp+=1
            self.tempBoard.append(row)
            temp+=1
            
        #Construct lines
        self.box=30 #box side length in pixels
        
        #Vertical lines
        temp=0
        while temp<=self.dim:
            x=self.base_x+temp*self.box
            self.lines.append([(x, self.base_y), (x, self.base_y+self.box*dim), (0,0,0)])
            temp+=1
        #Horizontal lines
        temp=0
        while temp<=self.dim:
            y=self.base_y+temp*self.box
            self.lines.append([(self.base_x, y), (self.base_x+self.box*dim,y), (0,0,0)])
            temp+=1

    def genTemp(self, board=False):
        #If fed another Grid instance "board," updates board as guess board
        #If board is unspecified, defaults to False and updates temp state from perm state
        if board!=False:
            for row in range(0,10):
                for col in range(0,10):
                    boardVal=board.board[row][col]
                    if boardVal==1 or boardVal==2 or boardVal==3:
                        self.tempBoard[row][col]=boardVal
                    else:
                        self.tempBoard[row][col]=self.board[row][col]
        else:
            for row in range(0,10):
                for col in range(0,10):
                    self.tempBoard[row][col]=self.board[row][col]

    def Update(self):
        #Updates the host rects list with data on each square on the board.
        #Data is taken from temp state matrix, not permanent one (changed 8/5/2012)
        #Stores this as a list item with the folowing format:
        # [ Pygame Rect of square , value of square ]
        #Updates top to bottom, left to right
        col=0
        while col<self.dim:
            row=0
            while row<self.dim:
                x=self.base_x+self.box*col
                y=self.base_y+self.box*row
                value=self.tempBoard[row][col]
                rect=Rect(x,y,self.box,self.box)
                #x, y of corner, width, height
                self.game.rects.append([rect, value])
                row+=1
            col+=1
            
    def addShip(self, points):
        (start,end)=points
        #Pass a set of points [(row,col), (row,col)]
        #Unpack start and end points
        (start_row,start_col)=start
        (end_row,end_col)=end
        #Check if start and end share a row, then construct a rectangle rowxcol based off that
        if end_row==start_row:
            if end_col>start_col:
                cols=range(start_col, end_col+1)
            else:
                cols=range(end_col, start_col+1)
            #The plus one anti-fenceposting, because range(0,2) only returns [0,1] not [0,1,2]
            #Two ranges, one for if the person clicks on a 2nd square to the left of the 1st click
            rows=[end_row]
        elif end_col==start_col:
            if end_row>start_row:
                rows=range(start_row, end_row+1)
            else:
                rows=range(end_row, start_row+1)
            #See above note, this time adjusting in case they click an end above the start
            cols=[end_col]
        for row in rows:
            for col in cols:
                self.board[row][col]=4
                #Set that square to contain an unshot ship
                
    def check(self, position):
        if position[0]<self.base_x or position[1]<self.base_y:
            return False
        elif position[0]>self.base_x+self.box*self.dim:
            return False
        elif position[1]>self.base_y+self.box*self.dim:
            return False
        else:
            x_box=int(floor((position[0]-self.base_x)/self.box))
            y_box=int(floor((position[1]-self.base_y)/self.box))
            return(y_box,x_box)

class Game:
    def __init__(self):
        self.size=(900,750)
        self.screen= pygame.display.set_mode(self.size, 0, 32)
        pygame.display.set_caption("Battleship: AI Edition--Is less more? Or is more more?")
        self.fps=25
        self.clock=pygame.time.Clock()

        #state codes
        self.running=True
        self.shipSet=True
        self.playing=False
        self.shipLoc=[(-1,-1),(-1,-1)]
        self.curBoard="none"
        self.state=[self.running,self.shipSet,self.playing,self.shipLoc,self.curBoard]

        self.drawcount=0
        self.rects=[]
        self.lines=[]
        self.boards=[]
        self.Board1=Grid((50,50),"P1 guess",10,self)
        self.Board2=Grid((550,50),"P2 guess",10,self)
        self.Board3=Grid((50,400),"P1 ships",10,self)
        self.Board4=Grid((550,400),"P2 ships",10,self)

        while self.running==True:
            events=pygame.event.get()
            for event in events:
                if event.type==QUIT:
                    self.running=False
                    pygame.display.quit()
            self.inputCheck(events)
            self.Update()
            if self.playing==True and self.drawcount%(3*self.fps)==0:
                (s_row,s_col)=self.pickShot(self.Board1,self.Board4)
                if self.Board4.board[s_row][s_col]==0:
                    self.Board4.board[s_row][s_col]=1
                    print "shooting at " + str((s_row,s_col)) + ", miss"
                    print self.Board4.board[s_row][s_col]
                elif self.Board4.board[s_row][s_col]==4:
                    self.Board4.board[s_row][s_col]=2
                    print "shooting at " + str((s_row,s_col)) + ", hit"
                    print self.Board4.board[s_row][s_col]
            self.Refresh()
            self.clock.tick(self.fps)
            self.drawcount+=1

    def isValid(board,square):
        s_row,s_col=sqjare
        if board.board
            
    def mouseCheck(self,pos):
        failboards=0 #Counter for number of boards square is not on
        for board in self.boards:
            #Run board check to see if it's on that board
            square=board.check(pos)
            if square:
                #It is, return that board's info and the square it's on
                return board,square
            else:
                #It's not, increment the count of boards it isn't on
                failboards+=1
        if failboards==4:
            #Square clicked is outside all active boards
            return False

    def inputCheck(self,events):
        for event in events:
            if event.type==MOUSEBUTTONDOWN:
                clicked=self.mouseCheck(event.pos)
                if self.shipSet==True:
                    if clicked and clicked[0]:
                        board=clicked[0]
                        square=clicked[1]
                        if self.shipLoc==[(-1,-1),(-1,-1)]:
                            self.shipLoc[0]=square
                            self.curBoard=board
                            self.curBoard.board[square[0]][square[1]]=4
                        elif self.shipLoc[1]==(-1,-1) and board==self.curBoard:
                            start=self.shipLoc[0]
                            if square[0]==start[0] or square[1]==start[1]:
                                self.shipLoc[1]=square
                                self.curBoard.addShip(self.shipLoc)
                                self.shipLoc=[(-1,-1),(-1,-1)]
                                self.curBoard="none"
                elif clicked:
                    grid=clicked[0]
                    board=grid.board
                    square=clicked[1]
                    row=square[0]
                    col=square[1]
                    board[row][col]=(board[row][col]+1)%6
            if event.type==KEYDOWN:
                if event.key==K_RETURN:
                    if self.shipSet==True:
                        self.shipSet=False
                        if self.shipLoc[0]!=(-1,-1):
                            self.curBoard.board[self.shipLoc[0][0]][self.shipLoc[0][1]]=0
                        self.curBoard="none"
                        self.shipLoc=[(-1,-1),(-1,-1)]
                    elif self.shipSet==False and self.playing==False:
                        self.shipSet=True
                if event.key==K_p:
                    if self.playing==False:
                        self.playing=True
                    elif self.playing==True:
                        self.playing=False

    def Update(self):
        self.Board1.genTemp(self.Board4) #Give P1 guess p2 actual board and update guess board
        self.Board2.genTemp(self.Board3) #Give P2 guess P1 actual board and update guess board
        self.Board3.genTemp()
        self.Board4.genTemp()

        #Over-ride temp board values for necesary squares
        if self.playing==False:
            pos=pygame.mouse.get_pos()
            hover=self.mouseCheck(pos)
            if hover and self.shipSet:
                board=hover[0]
                square=hover[1]
                if self.shipLoc==[(-1,-1),(-1,-1)]:
                    board.tempBoard[square[0]][square[1]]=5
                elif self.shipLoc[1]==(-1,-1):
                    if board==self.curBoard:
                        board.tempBoard[square[0]][square[1]]=4

    def pickShot(self,guess,real):
        guessboard=guess.tempBoard
        realboard=real.tempBoard
        targets=False
        if self.playing==True:
            hitlist=[]
            potlist=[]
            for row in range(0,10):
                for col in range(0,10):
                    cell=guessboard[row][col]
                    if cell==2:
                        hitlist.append((row,col))
                    if cell==0:
                        potlist.append((row,col))
            #shuffle(hitlist)
            #shuffle(potlist)
            shot=False
            for first in hitlist:
                if targets==False:
                    for second in hitlist:
                        if targets==False:
                            #finds horizontal pairs of hits
                            if first[0]==second[0] and (first[1]==second[1]-1 or first[1]==second[1]+1):
                                if first[1]>second[1]:
                                    first,second=second,first
                                print "found a row"
                                right=(second[0],second[1]+1)
                                left=(first[0],first[1]-1)
                                targets=[left,right]
                                print targets
                            #finds vertical pairs of hits
                            elif first[1]==second[1] and (first[0]==second[0]-1 or first[0]==second[0]+1):
                                if first[0]>second[0]:
                                    first,second=second,first
                                print "found a column"
                                above=(first[0]-1,first[1])
                                below=(second[0]+1,second[1])
                                targets=[above,below]
                                print targets
                    if targets==False:
                        print "no row or col"
                        left=(first[0],first[1]-1)
                        right=(first[0],first[1]+1)
                        above=(first[0]-1,first[1])
                        below=(first[0]+1,first[1])
                        targets=[left,right,above,below]
                        print targets
                    #shuffle(targets)
                    for point in targets:
                        if point in potlist and shot==False:
                            shot=point
                            print shot
            if targets==False:
                print "no hits"
                shot=potlist[0]
        return(shot)

    def Refresh(self):
        #Fill screen with background color (white atm)
        self.screen.fill( (255,255,255))

        del self.rects[:] #Empty the list of old rectangles
        #Tell all Grids to update their rectangle data
        for board in self.boards:
            board.Update()
        
        #Draw rectangles to screen by filling rects of squares
        for rect in self.rects:
            box=rect[0]
            value=rect[1]
            if value==0:
                color=(127,255,212)
            elif value==1:
                color=(255,255,255)
            elif value==2:
                color=(255,0,0)
            elif value==3:
                color=(178,34,34)
            elif value==4:
                color=(139,139,139)
            elif value==5:
                color=(255,255,0)
            self.screen.fill(color, box)

        #Draw lines to the screen
        for line in self.lines:
            start_pos=line[0]
            end_pos=line[1]
            color=line[2]
            pygame.draw.line(self.screen, color, start_pos, end_pos, 2)

        #Flip the screen to update changes
        pygame.display.flip()
        return()

theGame=Game() #I just lost the game
