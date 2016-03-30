import pygame
from pygame.locals import *
import random
import math
from math import *

pygame.init()

class Grid:
    def __init__(self,location,name,dim,lines,rects,boards):
        #Unpack location into x and y co-ordinates of upper left corner
        self.base_x=location[0]
        self.base_y=location[1]
        self.dim=dim
        self.name=name
        boards.append(self)
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

        #Construct lines
        self.box=30 #box side length in pixels
        
        #Vertical lines
        temp=0
        while temp<=self.dim:
            x=self.base_x+temp*self.box
            lines.append([(x, self.base_y), (x, self.base_y+self.box*dim), (0,0,0)])
            temp+=1
        #Horizontal lines
        temp=0
        while temp<=self.dim:
            y=self.base_y+temp*self.box
            lines.append([(self.base_x, y), (self.base_x+self.box*dim,y), (0,0,0)])
            temp+=1
            
    def Update(self):
        #Updates the host rects list with data on each square on the board.
        #Stores this as a list item with the folowing format:
        # [ Pygame Rect of square , value of square ]
        #Updates left to right, top to bottom
        row=0
        while row<self.dim:
            col=0
            while col<self.dim:
                x=self.base_x+self.box*col
                y=self.base_y+self.box*row
                value=self.board[row][col]
                rect=Rect(x,y,self.box,self.box) #x, y of corner, width, height
                rects.append([rect, value])
                col+=1
            row+=1
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
            return(x_box,y_box)

def Refresh():
    #Fill screen with background color (white atm)
    screen.fill( (255,255,255))

    del rects[:] #Empty the list of old rectangles
    #Tell all Grids to update their rectangle data
    for board in boards:
        board.Update()

    #Draw rectangles to screen by filling rects of squares
    for rect in rects:
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
        screen.fill(color, box)

    #Draw lines to the screen
    for line in lines:
        start_pos=line[0]
        end_pos=line[1]
        color=line[2]
        pygame.draw.line(screen, color, start_pos, end_pos, 2)

    #Flip the screen to update changes
    pygame.display.flip()

def mouse_check(pos):
    failboards=0
    for board in boards:
        square=board.check(event.pos)
        if square:
            return board,square
        else:
            failboards+=1
        if failboards==4:
            print "YOU FAIL"
            return False

        
size=(900,750)
screen= pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Battleship: AI Edition--Is less more? Or is more more?")
fps=25
clock=pygame.time.Clock()

running=True

drawcount=0
rects=[]
lines=[]
boards=[]
Board1=Grid((50,50), "P1 guess", 10, lines,rects,boards)
Board2=Grid((550,50), "P2 guess", 10, lines,rects,boards)
Board3=Grid((50,400), "P1 ships", 10, lines,rects,boards)
Board4=Grid((550,400), "P2 ships", 10, lines,rects,boards)


while running==True:
    events=pygame.event.get()
    for event in events:
        if event.type==QUIT:
            running=False
            pygame.display.quit()
        if event.type==MOUSEBUTTONDOWN:
            clicked=mouse_check(event.pos)
            if clicked:
                board=clicked[0].board
                square=clicked[1]
                row=square[0]
                col=square[1]
                board[row][col]=(board[row][col]+1)%5
            
    clock.tick(fps)
    Refresh()
    drawcount+=1
