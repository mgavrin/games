import pygame
from pygame.locals import *
import os

class zFilter:
    def __init__(self,hair,eye,nose,foot):
        self.features={"hair":hair,"eye":eye,"nose":nose,"foot":foot}
        for feature in self.features.keys():
            trait=self.features[feature]
            if trait == "blank" or trait=="rotator" or trait == None:
                pass
            elif self.features[feature] in rotationLists[feature]:
                pass
            else:
                print trait, feature, self.features
                print "Invalid input! "+trait+" is not a valid "+feature
    def __getitem__(self,key):
        return self.features[key]

    def __eq__(self,other):
        for key in self.features.keys():
            if self[key]!=other[key]:
                return False
        return True

    def __str__(self):
        out=""
        for feature in ["hair","eye","nose","foot"]:
            out+=self.features[feature]
            out+=" "
        return out

    def rotateForward(self,feature):
        if feature=="hair":
            rotator=hairRotator
        elif feature=="eye":
            rotator=eyeRotator
        elif feature=="nose":
            rotator=noseRotator
        elif feature=="foot":
            rotator=footRotator
        options=list(rotator)+["rotator","blank"]
        curInd=options.index(self.features[feature])
        newInd=(curInd+1)%7
        self.features[feature]=options[newInd]

    def rotateBackward(self,feature):
        if feature=="hair":
            rotator=hairRotator
        elif feature=="eye":
            rotator=eyeRotator
        elif feature=="nose":
            rotator=noseRotator
        elif feature=="foot":
            rotator=footRotator
        options=list(rotator)+["rotator","blank"]
        curInd=options.index(self.features[feature])
        newInd=(curInd-1)%7
        self.features[feature]=options[newInd]

    def changeToMatch(self,other):
        for feature in other.features:
            self.features[feature]=other.features[feature]

    def reset(self):
        for feature in self.features:
            self.features[feature]="blank"

    def drawToScreen(self,screen):
        result=pygame.Surface((60,120),pygame.SRCALPHA,32)
        result.blit(hairImages[self.features["hair"]],(0,0))
        result.blit(eyeImages[self.features["eye"]],(0,40))
        result.blit(noseImages[self.features["nose"]],(0,70))
        result.blit(footImages[self.features["foot"]],(0,90))
        return result
        
    

def evaluateStack(filters):
    #filters: initial zoombini or crystal,
    #then all filters from outside to inside
    if len(filters)>4:
        print "Illegal operation: excessive filters"
    output=zFilter(None,None,None,None)
    for feature in ["hair","eye","nose","foot"]:
        output.features[feature]=evaluateFeature(feature,filters)
    return output

def evaluateFeature(feature,filters):
    output=None
    for f in filters:
        val=f[feature]
        if val=="rotator":
            rotationList=rotationLists[feature]
            prevIndex=rotationList.index(output)
            output=rotationList[(prevIndex+1)%len(rotationList)]
        elif val!="blank":
            output=val
    return output
    
def evaluateSidePermutations(instuff,zoombini1,zoombini2):
    #output should be list of tuples of zFilters
    output=[]
    permutations=permute3(instuff)
    for permutation in permutations:
        filters=permutation[0]
        recipe=permutation[1]
        tempOut1=evaluateStack([zoombini1]+filters)
        tempOut2=evaluateStack([zoombini2]+filters)
        output.append( [(tempOut1,tempOut2),recipe] )
    return output

def permute3(instuff):
    filters=instuff[0]
    filterNames=instuff[1]
    splits=[]
    #no filters
    splits.append([])
    #permutations of 1 filter
    splits.append([0])
    splits.append([1])
    splits.append([2])
    #permutations of 2 filters
    splits.append([0,1])
    splits.append([0,2])
    splits.append([1,0])
    splits.append([1,2])
    splits.append([2,0])
    splits.append([2,1])
    #Permutations of 3 filters
    splits.append([0,1,2])
    splits.append([0,2,1])
    splits.append([1,0,2])
    splits.append([1,2,0])
    splits.append([2,0,1])
    splits.append([2,1,0])
    
    output=[]
    for split in splits:
        tmplist=[]
        nameString=""
        for i in split:
            tmplist.append(filters[i])
            nameString+=str(filterNames[i])
        output.append([tmplist,nameString])
    return output

def checkForSolutions(zoombini1,zoombini2,goal1,goal2,inputFilters):
    #zoombini 1 and 2 are the zoombinis on the left
    #goal 1 and 2 are the whole-zoombini crystals on the right
    halfCombinations=splitFilters(inputFilters)
    combinations=[]
    for combo in halfCombinations:
        combinations.append(combo)
        combinations.append([combo[1],combo[0]])
    #combination is an exhaustive list of lists of lists:
    #the second-level lists are pairs:
    #[[set of filters on left],[set of filters on right]]
    for combination in combinations:
        leftResults=evaluateSidePermutations(combination[0],zoombini1,zoombini2)
        rightResults=evaluateSidePermutations(combination[1],goal1,goal2)
        for leftRes in leftResults:
            for rightRes in rightResults:
                (leftOut,leftRecipe)=leftRes
                (rightOut,rightRecipe)=rightRes
                if leftOut[0]==rightOut[0] and leftOut[1]==rightOut[1]:
                    print "This instance is solvable! Recipe:"
                    print "   Left filters: ", [x for x in leftRecipe]
                    print "   Right filters:", [x for x in rightRecipe]
                    return (leftRecipe,rightRecipe)
    print "This instance is not solvable."


def splitFilters(f): 
    splits=[] 
    splits.append(["012","345"]) #0: ABC DEF 
    splits.append(["013","245"]) #1: ABD CEF 
    splits.append(["014","235"]) #2: ABE CDF 
    splits.append(["015","234"]) #3: ABF CDE 
    splits.append(["023","145"]) #4: ACD BEF 
    splits.append(["024","135"]) #5: ACE DBF 
    splits.append(["025","134"]) #6: ACF DBE 
    splits.append(["123","045"]) #7: BCD AEF 
    splits.append(["124","035"]) #8: BCE ADF 
    splits.append(["125","034"]) #9: BCF ADE 

    output=[]
    for split in splits: 
        outleft=[] 
        outright=[] 
        for char in split[0]: 
            outleft.append( f[ int(char) ]) 
        for char in split[1]: 
            outright.append( f[ int(char) ]) 
        output.append( [[outleft,split[0]] , [outright,split[1]]] ) 
    return output

hairRotator=["pony","tuft","flat","cap","fluff"]
eyeRotator=["dot","sleepy","shades","specs","cyclops"]
noseRotator=["red","green","blue","yellow","pink"]
footRotator=["shoes","skates","wheels","prop","spring"]
rotationLists={"hair":hairRotator,"eye":eyeRotator,
              "nose":noseRotator,"foot":footRotator}


class screen:
    def __init__(self,inFilters=None):
        self.width=488
        self.height=356
        pygame.init()
        self.screenSize=(self.width,self.height)
        self.gameScreen=pygame.display.set_mode(self.screenSize,0,32)
        self.tmpScreen=pygame.Surface((650,475),0,32)
        self.backdrop=pygame.image.load("Backdrop1.png")
        self.gameScreen.blit(self.backdrop,(0,0))
        pygame.display.flip()
        self.gameSlice=pygame.Surface(self.screenSize)
        self.clock=pygame.time.Clock()
        self.fps=36

        self.aLeft=230
        self.aTop=135
        self.aRight=350
        self.aBottom=185
        self.rLeft=247
        self.rTop=70
        self.rRight=333
        self.rBottom=110
        
        self.zoombini1=zFilter("blank","blank","blank","blank")
        self.zoombini1.drawPos=(40,30)
        self.zoombini2=zFilter("blank","blank","blank","blank")
        self.zoombini2.drawPos=(120,30)
        self.goal1=zFilter("blank","blank","blank","blank")
        self.goal1.drawPos=(40,170)
        self.goal2=zFilter("blank","blank","blank","blank")
        self.goal2.drawPos=(120,170)
        self.filters=[]
        for i in range(0,6):
            newFilter=zFilter("blank","blank","blank","blank")
            if i<3:
                newFilter.drawPos=(400+i*80,30)
            else:
                newFilter.drawPos=(400+(i-3)*80,170)
            self.filters.append(newFilter)
        self.outFilters=[]
        for i in range(0,6): #outFilters
            newOutFilter=zFilter("blank","blank","blank","blank")
            if i<3:
                newOutFilter.drawPos=(60+(i)*80,330)
            else:
                newOutFilter.drawPos=(380+(i-3)*80,330)
            self.outFilters.append(newOutFilter)
        self.allFilters=[self.zoombini1,self.zoombini2,self.goal1,self.goal2]+self.filters+self.outFilters
        self.buttonTozFilter={11:self.zoombini1,12:self.zoombini2,13:self.filters[0],
                              14:self.filters[1],15:self.filters[2],21:self.goal1,
                              22:self.goal2,23:self.filters[3],24:self.filters[4],
                              25:self.filters[5]}

        if inFilters:
            self.zoombini1.changeToMatch(inFilters[0])
            self.zoombini2.changeToMatch(inFilters[1])
            self.goal1.changeToMatch(inFilters[2])
            self.goal2.changeToMatch(inFilters[3])
            for i in range(0,len(self.filters)):
                self.filters[i].changeToMatch(inFilters[i+4])
        
        self.running=True
        self.mainloop()

    def mainloop(self):
        while self.running:            
            events=pygame.event.get()
            self.processInput(events)
            self.drawScreen()
            self.clock.tick(self.fps)
        pygame.display.quit()

    def processInput(self,events):
        for event in events:
            if event.type==QUIT:
                self.running=False
                break
            elif event.type==MOUSEBUTTONDOWN:
                thingClickedOn=self.getClickedOn(event.pos)
                if isinstance(thingClickedOn,tuple):#zFilter and name of part
                    if event.button==1:
                        thingClickedOn[0].rotateForward(thingClickedOn[1])
                    elif event.button==3:
                        thingClickedOn[0].rotateBackward(thingClickedOn[1])
                elif thingClickedOn=="analyze button":
                    for fil in self.outFilters:
                        fil.reset()
                    recipes=checkForSolutions(self.zoombini1,self.zoombini2,self.goal1,self.goal2,self.filters)
                    if recipes is not None:
                        (leftRecipe,rightRecipe)=recipes
                        for i in range(0,len(leftRecipe)):
                            self.outFilters[i].changeToMatch(self.filters[int(leftRecipe[i])])
                        for i in range(0,len(rightRecipe)):
                            self.outFilters[5-i].changeToMatch(self.filters[int(rightRecipe[i])])
                elif thingClickedOn=="reset button":
                    for fil in self.allFilters:
                        fil.reset()
                    
        

    def drawScreen(self):
        self.tmpScreen.blit(self.backdrop,(0,0))
        for fil in self.allFilters:
            filterPicture=fil.drawToScreen(self)
            self.tmpScreen.blit(filterPicture,fil.drawPos)
        self.gameScreen.blit(pygame.transform.scale(self.tmpScreen,(self.width,self.height)),(0,0))
        pygame.display.flip()

    def getClickedOn(self,coords):
        xScale=self.tmpScreen.get_width()/float(self.gameScreen.get_width())
        yScale=self.tmpScreen.get_height()/float(self.gameScreen.get_height())
        x=coords[0]
        x*=xScale
        y=coords[1]
        y*=yScale
        if self.aLeft<x<self.aRight and self.aTop<y<self.aBottom:
            return "analyze button"
        if self.rLeft<x<self.rRight and self.rTop<y<self.rBottom:
            return "reset button"
        clicked=0
        feature=None
        if 40<x<100:
            clicked+=1
        elif 120<x<180:
            clicked+=2
        elif 400<x<460:
            clicked+=3
        elif 480<x<540:
            clicked+=4
        elif 560<x<620:
            clicked+=5
        if 30<y<150:
            clicked+=10
            y-=30
        elif 170<y<290:
            clicked+=20
            y-=170
        if clicked==0:
            return None
        if y>90:
            feature="foot"
        elif y>70:
            feature="nose"
        elif y>40:
            feature="eye"
        elif y>0:
            feature="hair"
        if clicked in self.buttonTozFilter:
            return (self.buttonTozFilter[clicked],feature)
        else:
            return None
    

blank=pygame.image.load(os.path.join("FeaturePics","blank.png"))
rotator20=pygame.image.load(os.path.join("FeaturePics","rotator20.png"))
rotator30=pygame.image.load(os.path.join("FeaturePics","rotator30.png"))
rotator40=pygame.image.load(os.path.join("FeaturePics","rotator40.png"))

fluff=pygame.image.load(os.path.join("FeaturePics","fluff.png"))
cap=pygame.image.load(os.path.join("FeaturePics","cap.png"))
tuft=pygame.image.load(os.path.join("FeaturePics","tuft.png"))
flat=pygame.image.load(os.path.join("FeaturePics","flat.png"))
pony=pygame.image.load(os.path.join("FeaturePics","pony.png"))
hairImages={"fluff":fluff,"cap":cap,"flat":flat,"pony":pony,"tuft":tuft,"blank":blank,"rotator":rotator40}

sleepy=pygame.image.load(os.path.join("FeaturePics","sleepy.png"))
shades=pygame.image.load(os.path.join("FeaturePics","shades.png"))
dot=pygame.image.load(os.path.join("FeaturePics","dot.png"))
specs=pygame.image.load(os.path.join("FeaturePics","specs.png"))
cyclops=pygame.image.load(os.path.join("FeaturePics","cyclops.png"))
eyeImages={"sleepy":sleepy,"shades":shades,"dot":dot,"cyclops":cyclops,"specs":specs,"blank":blank,"rotator":rotator30}

red=pygame.image.load(os.path.join("FeaturePics","red.png"))
yellow=pygame.image.load(os.path.join("FeaturePics","yellow.png"))
green=pygame.image.load(os.path.join("FeaturePics","green.png"))
blue=pygame.image.load(os.path.join("FeaturePics","blue.png"))
pink=pygame.image.load(os.path.join("FeaturePics","pink.png"))
noseImages={"red":red,"yellow":yellow,"green":green,"blue":blue,"pink":pink,"blank":blank,"rotator":rotator20}

spring=pygame.image.load(os.path.join("FeaturePics","spring.png"))
prop=pygame.image.load(os.path.join("FeaturePics","prop.png"))
wheels=pygame.image.load(os.path.join("FeaturePics","wheels.png"))
skates=pygame.image.load(os.path.join("FeaturePics","skates.png"))
shoes=pygame.image.load(os.path.join("FeaturePics","shoes.png"))
footImages={"spring":spring,"prop":prop,"wheels":wheels,"skates":skates,"shoes":shoes,"blank":blank,"rotator":rotator40}






zoombini1=zFilter("cap","cyclops","green","shoes")
zoombini2=zFilter("tuft","dot","green","skates")
goal1=zFilter("fluff","dot","pink","shoes")
goal2=zFilter("flat","sleepy","blue","skates")
filters=[]
filters.append(zFilter("blank","blank","blank","prop"))
filters.append(zFilter("rotator","blank","blue","blank"))
filters.append(zFilter("blank","rotator","blue","blank"))
filters.append(zFilter("blank","cyclops","blank","spring"))
filters.append(zFilter("cap","blank","red","blank"))
filters.append(zFilter("fluff","blank","blank","blank"))
inFilters=[zoombini1,zoombini2,goal1,goal2]+filters
s=screen(inFilters)
