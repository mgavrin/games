    def update(self):
        #Updates all adjacency lists, bomb counts, and square's clear status

        self.numBombsFlagged=0
        self.UndugAdjacents=[]
        
        for Square in self.adjacentSquares:
            #Recount the number of tangent player-flagged squares
            if Square.displayState=="f":
                self.BombsFlagged+=1
            #Add undug squares to a list
            if square.displayState=="u":
                self.UndugAdjacents.append(Square)
        #Remaining bombs is the difference of flagged bombs and tangent bombs
        self.numBombsRemaining = self.value - self.numBombsFlagged
        

        #Check if this square is now clear
        if self.numBombsRemaining<=0 and self.displayState=="d":
            self.isClear=True
            if self.value=="b":
                print "you fucked up if this is showing."
        else:
            self.isClear=False

    def doBasicDigLogic(self):
        if self.isClear:
            for Square in self.UndugAdjacents:
                Square.dig()
        elif self.numBombsRemaining==len(self.UndugAdjacents):
            for Square in self.UndugAdjacents:
                Square.flag()
